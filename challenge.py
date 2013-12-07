import os
import collections

class User:
    def __init__(self):
        self.first, self.last, self.amount = None, None, 0
    def __str__(self):
        return '%s, %s: %s' % (self.last, self.first, self.amount)
        
#source_dir = r'C:\CloudShareCodeChallenge\Sample'
source_dir = r'C:\CloudShareCodeChallenge\Challenge'
dct_log_files_by_prefix = {}
dct_top_paying_users_for_prefix = {} # {uid -> User}
dct_top_paying_users_ever = {} # {uid -> User}
dct_user_names_for_prefix = {} # {uid -> (first, last)}
set_payments_already_seen_for_current_prefix = set()
dct_first_names = collections.defaultdict(int) # {name -> count}
num_double_bookings = 0
num_total_paymants = 0
num_files_parsed = 0

# prepare {prefix -> [filenames]}
for filename in os.listdir(source_dir):
    try:
        prefix = filename.split('_')[1] 
        dct_log_files_by_prefix.setdefault(prefix, []).append(filename)
    except IndexError:
        pass

for prefix, filenames in dct_log_files_by_prefix.iteritems():
    for filename in filenames:
        num_files_parsed += 1
        file_path = os.path.join(source_dir, filename)
        #print 'parsing file:', file_path
        with open(file_path) as f:
            for record in f:
                if record.startswith('UR'):
                    _, user_id, first_name, last_name = record.split(',')
                    #print 'user:', first_name, last_name
                    dct_user_names_for_prefix[user_id] = (first_name, last_name.strip())
                    dct_first_names[first_name] += 1
                    
                else: #payment
                    num_total_paymants += 1
                    _, payment_id, user_id , amount = record.split(',')
                    if payment_id not in set_payments_already_seen_for_current_prefix:
                        set_payments_already_seen_for_current_prefix.add(payment_id)
                        # add the user or update it. no duplicate payments arrive here
                        user = dct_top_paying_users_for_prefix.setdefault(user_id, User())
                        user.amount += int(amount)
                    else:
                        num_double_bookings += 1
        print 'number of files parsed so far:', num_files_parsed

    # done with all files for that prefix
    set_payments_already_seen_for_current_prefix = set()
    # calculate top ten
    dct_top_paying_users_ever.update(dct_top_paying_users_for_prefix)
    pairs = list(dct_top_paying_users_ever.iteritems())
    pairs.sort(key=lambda x : x[1].amount, reverse=True) # sort by sum descending
    pairs = pairs[:10] # leave only top ten
    dct_top_paying_users_ever = dict(pairs)
    # update the names of top ten users
    for uid, user in dct_top_paying_users_ever.iteritems():
        if uid in dct_user_names_for_prefix:
            # it might be that we did not encounter the user id yet
            user.first = dct_user_names_for_prefix[uid][0]
            user.last = dct_user_names_for_prefix[uid][1]
    
with open(r'C:\CloudShareCodeChallenge\Work\results.txt', 'w+') as f:
    f.write('top 10 users:\n')
    lst_sorted_top_ten = list(dct_top_paying_users_ever.iteritems())
    lst_sorted_top_ten.sort(key=lambda x : x[1].amount, reverse=True)
    for x in lst_sorted_top_ten:
        f.write(str(x[1]) + '\n')
    
    
    min_freq = min(dct_first_names.itervalues())
    max_freq = max(dct_first_names.itervalues())
    set_most_freq_names = set()
    set_least_freq_names = set()
    for first_name, count in dct_first_names.iteritems():
        if count == max_freq:
            set_most_freq_names.add(first_name)
        if count == min_freq:
            set_least_freq_names.add(first_name)
    f.write('most frequent names:\n')
    for name in set_most_freq_names:
        f.write('{0!s}, {1!s}\n'.format(name, max_freq))
    f.write('least frequent names:\n')
    for name in set_least_freq_names:
        f.write('{0!s}, {1!s}\n'.format(name, min_freq))
    
    f.write('double bookings: {0!s}/{1!s}\n'.format(num_double_bookings, num_total_paymants))
    
    
    
        

    