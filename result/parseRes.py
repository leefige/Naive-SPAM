import re

for i in range(21, 25):
    with open("final3.txt", mode='a', encoding='utf-8') as fout:
        with open(str(i)+".txt", mode='r') as fin:
            print("parsing %d" % i)
            start = False
            has = False
            for line in fin:
                line = line.strip()
                if not start:
                    if line == "Validating...":
                        start = True
                else:
                    try:
                        if re.match(r'.*accuracy: (\d.*\d)',  line):
                            accRe = re.search(r'(0\.\d*\d)', line, flags=0)
                            if accRe:
                                has = True
                                acc = accRe.group(0)
                        elif re.match(r'SPAM:.*',  line):
                            spRe = re.findall(r'(\d\.\d+\d)', line, flags=0)
                            if spRe:
                                pre_spam = spRe[0]
                                rec_spam = spRe[1]
                                f1_spam = spRe[2]
                        elif re.match(r'HAM:.*', line):
                            spRe = re.findall(r'(\d\.\d+\d)', line, flags=0)
                            if spRe:
                                pre_ham = spRe[0]
                                rec_ham = spRe[1]
                                f1_ham = spRe[2]
                    except IndexError:
                        print(pre_spam)
            if has:
                fout.write("%s, %s, %s, %s, %s, %s, %s\n" % (acc, pre_spam, rec_spam, f1_spam, pre_ham, rec_ham, f1_ham))
                        