import boto.ec2.elb
import time

b_actuall_run = True
b_create_sec_groups = True

def _get_all_running_instances(connection):
    lst_all_reservations = connection.get_all_instances()
    lst_instances = []
    for res in lst_all_reservations:
        for inst in res.instances:
            if inst.state in ["running"]: 
                lst_instances.append(inst)
    return lst_instances

def configure_instances(connection, sec_group_name, b_terminate):
    ami_id = 'ami-7ae68013'
    key_name = 'drupal-key-pair'
    instances_per_zone = 2
    lst_available_zones = connection.get_all_zones()
    if not b_terminate:
        print 'available zones:'
        for num, zone in enumerate(lst_available_zones):
            print '{}) {}'.format(num, zone.name)
        first_zone_index = raw_input('choose first availability zone:')
        second_zone_index = raw_input('choose first availability zone:')
        
        first_zone = lst_available_zones[int(first_zone_index)]
        second_zone = lst_available_zones[int(second_zone_index)]
        lst_zone_names = [first_zone.name, second_zone.name]
        
    
    lst_all_reservations = connection.get_all_instances()
    for res in lst_all_reservations:
        for inst in res.instances:
            if b_terminate or inst.placement in lst_zone_names:
                if inst.state not in ["terminated", "shutting-down"]:
                    if b_terminate:
                        print 'terminating {}'.format(inst)
                        inst.terminate()
                    else:
                        print 'there are already non- terminated instances in selected zones.\nplease terminate them first'
                        quit()
    if b_terminate:
        return [], []                
    for zone in (first_zone, second_zone):
        print 'creating {} instances in {}'.format(instances_per_zone, zone.name)
        if b_actuall_run:
            res = connection.run_instances(ami_id, key_name=key_name,
                                           instance_type='t1.micro',
                                           security_groups=[sec_group_name],
                                           min_count=instances_per_zone,
                                           max_count=instances_per_zone,
                                           placement=zone.name)
            print 'got reservation: {} instances: {}'.format(res, res.instances)
    lst_instances = []
    while not len(lst_instances) == 4:
        print 'waiting for instances to run... ({} running)'.format(len(lst_instances))
        time.sleep(5)
        lst_instances = _get_all_running_instances(connection)
    return lst_zone_names, lst_instances

def ensure_security_group_exists(conn, b_terminate):
    if b_terminate:
        return None
    print 'verifying security group exists'
    group_name, group_desc = 'hw1', 'security group for web (hw1)'
    lst_all_groups = conn.get_all_security_groups()
    if group_name not in (gr.name for gr in lst_all_groups):
        print 'creating a new security group'
        if b_create_sec_groups:
            web_security_group = conn.create_security_group(group_name, group_desc)
            rule1 = web_security_group.authorize('tcp', 80, 80, '0.0.0.0/0')
            rule2 = web_security_group.authorize('tcp', 443, 443, '0.0.0.0/0')
            if (rule1, rule2) != (True, True):
                raise Exception('security group configuration failed')
            assert group_name in (gr.name for gr in conn.get_all_security_groups())
        print 'security group {} created'.format(web_security_group)
    else:
        print 'security group already exists'
    return group_name

def configure_load_balancer(elb_conn, lst_zone_names, lst_instance_ids, b_terminate):
    lst_ports = [(80, 80, 'http'), (443, 443, 'tcp')]
    lst_balancers = elb_conn.get_all_load_balancers()
    balancer_name = 'my-lb'
    if lst_balancers:
        if b_terminate:
            for lb in lst_balancers:
                print 'terminating balancer {}'.format(lb)
                lb.delete()
            return  
        else:
            print 'there is already a load balancer. delete it first'
            quit()
    if not b_terminate:
        # create a balancer
        balancer = elb_conn.create_load_balancer(balancer_name, lst_zone_names, lst_ports)
        print 'load balancer created'
        print 'you can access it via: {}'.format(balancer.dns_name)
        # connect instances
        print 'registering instances'
        balancer.register_instances(lst_instance_ids)


def load_config():
    boto.config.load_from_path('/home/ido/.boto')

def configure_ec2(b_terminate):
    load_config()
    region_name = 'us-east-1'
    ec2_conn = boto.ec2.connect_to_region(region_name)
    group_name = ensure_security_group_exists(ec2_conn, b_terminate)
    # create 2 pairs of instances (in two given availability zones zones chosen by user)
    lst_zone_names, lst_instances = configure_instances(ec2_conn, group_name, b_terminate)
    # create a load balancer
    elb_conn = boto.ec2.elb.connect_to_region(region_name)
    configure_load_balancer(elb_conn,
                         lst_zone_names,
                         [inst.id for inst in lst_instances],
                         b_terminate)

if __name__ == '__main__':
    import sys
    b_terminate = 'terminate' in sys.argv
    configure_ec2(b_terminate)