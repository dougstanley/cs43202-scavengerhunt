#!/usr/bin/env python2
import sys
import os.path
import tarfile
import re
from hashlib import md5

H = {'0fd9fed103a04059b3a32880adc7103f': 'd27a7bb9639f7e4e6dc5fa80d5e43ddd',
     '1354959c8917d903aece9628069e2cd9': '4433f1a2f273547c22eb38484f9bf781',
     '15f74ad38d0d02ee79ab8581b8290391': 'a70fc191848661ef8cd9b3bec7bb5434',
     '23cbb416b75214b1b72d4512542e94db': '3ba7e62f51d4dcd6653d73b92ca383c5',
     '47878e4acf108bd270148e880eb70c9d': 'e606bcd4028a15da85261384123fc8a1',
     '52af43fc4594de83e5d295a114d63792': '24d395f0bcc214437992517573590433',
     '6f680beaed4f85cf2537bb57fb54c82d': '1c87b6e66cb159f511726d73dd61e8fc',
     '6f84a451784b3224a7e41a023b98e145': '3c821c0133b3e153d10a0702e522d4f5',
     '8708674be6116a2999ae33ee2f8b8689': 'ebb14a7c5cae35316985f7c88e78106a',
     '8b2cecb2c55793780d8ba61e74621023': '00b2692a6f5d0d3571b74ce8636b8411',
     '8cbef730f670e2344c93000e0d5ce375': 'fe466c33b35c6e675499f37017a647a7',
     'bbbf8ecc2122ebfa64533bc66bc5d825': '6382c575dffd6166e7c3ec8b1d567cb4',
     'bc110b3f8ebb4358ab77db1469e94abc': '39910ce68f4e85c64bf96da17e3cebcb',
     'c1cd60793c97bec32ab7cd9d02fe1753': '0daf7a8e9a47f6917bba40e00a0e95d9',
     'c531aba63d31f5693d756e083908d787': 'de904a0333f95a4b42d6ef695986ce3a',
     'ef4bf2e9f610949de6760b6d1af39e55': '81534a9e8f631c09f03969b38bf0b439'}

R = {'aed0ee6a3273fa7619c62258f6112ac4': (r'^.*EXPLODING KITTEN.+?8ca92bd53c' +
                                          r'ba946e.+?burried.+rando.+?cat fi' +
                                          r'le\.jpg.+nope.+aes256.+Final Sub' +
                                          r'.+hunt\.tar.+submit\.sh.+blackb' +
                                          r'oard.+?Congrat.+$'),
     '1bf3a32e8b4488491faeea0d9f0f48cc': (r'^.+RAINBOW RALPHING CAT.+?Congra' +
                                          r'ts.+?ring..rainbow.+?meminfo.+Me' +
                                          r'mTotal.+SwapTotal.+Clue.+md5sum' +
                                          r'.+pipe.+?hash.+explodingkitten.+' +
                                          r'Luck.+?$'),
     '1e54c6d1e9c2de0d35f6946b768b9922': r'^Mem|Swap.+[0-9] kB$',
     'c6176cbf7c2a0a975338270467f05d2e': (r'^(?=.*?(vendor_id\s+?:\s+\w+))' +
                                          '(?=.*?(flags\s+:\s+[a-z ]+)).*$'),
     }

NO_REG = ('52af43fc4594de83e5d295a114d63792',
          '1354959c8917d903aece9628069e2cd9',
          '8cbef730f670e2344c93000e0d5ce375',
          '15f74ad38d0d02ee79ab8581b8290391',
          'c531aba63d31f5693d756e083908d787',
          'ef4bf2e9f610949de6760b6d1af39e55',
          '6f84a451784b3224a7e41a023b98e145',
          '8708674be6116a2999ae33ee2f8b8689',
          '47878e4acf108bd270148e880eb70c9d',
          'c1cd60793c97bec32ab7cd9d02fe1753',
          'bc110b3f8ebb4358ab77db1469e94abc',
          'bbbf8ecc2122ebfa64533bc66bc5d825',
          'e47f9c6e75a8d6291ecbea7cf7da5622',
          '79eb022bb34e82b7e5bcbbd78d142957',
          'cb515018cc256d2e5307016885e0e32b',
          )

NO_HASH = ('79eb022bb34e82b7e5bcbbd78d142957',
           'cb515018cc256d2e5307016885e0e32b',
           '1bf3a32e8b4488491faeea0d9f0f48cc',
           'aed0ee6a3273fa7619c62258f6112ac4',
           'c6176cbf7c2a0a975338270467f05d2e',
           '1e54c6d1e9c2de0d35f6946b768b9922',
           'e47f9c6e75a8d6291ecbea7cf7da5622',
           )

ALL = ('e47f9c6e75a8d6291ecbea7cf7da5622',
       '0fd9fed103a04059b3a32880adc7103f',
       '23cbb416b75214b1b72d4512542e94db',
       '6f680beaed4f85cf2537bb57fb54c82d',
       '8b2cecb2c55793780d8ba61e74621023',
       ) + NO_REG + NO_HASH

SPECIAL_CASES = ('79eb022bb34e82b7e5bcbbd78d142957',
                 'e47f9c6e75a8d6291ecbea7cf7da5622',
                 'cb515018cc256d2e5307016885e0e32b',
                 )


class GradingError(Exception):
    pass


class Submission(object):
    def __init__(self, tar_archive):
        self.__score = 0
        self.__map = {}
        self.__tar = None
        try:
            self.__tar = tarfile.open(tar_archive, 'r')
            for name in self.__tar.getnames():
                self.__map[name] = md5(name).hexdigest()
        except Exception, e:
            print "Failed to open tarfile: %s" % tar_archive
            print "Error given: %s" % str(e)
            sys.exit(1)

    def __del__(self):
        if self.__tar is not None:
            self.__tar.close()

    def __check_all_files(self):
        no_hash = set(NO_HASH)
        no_reg = set(NO_REG)
        all_files = set(ALL)
        all_good = True

        if not self.__check_file_sets:
            all_good = False
            print "Some expected files not found in submission!"

        for f in self.__tar:
            key = self.__map[f.name]
            if f.isdir() or key in SPECIAL_CASES:
                continue
            elif key in all_files.difference(no_hash):
                # check file against hash value
                fp = self.__tar.extractfile(f)
                fhash = md5(fp.read()).hexdigest()
                fp.close()
                if fhash != H[key]:
                    all_good = False
                    print f.name, "does not match what is expected!"
                else:
                    self.__score += 2
            elif key in all_files.difference(no_reg):
                # Check file against regex
                if key in R:
                    fp = self.__tar.extractfile(f)
                    m = re.match(R[key], fp.read(), re.S | re.M)
                    fp.close()
                    if m is None:
                        all_good = False
                        print f.name, "does not match regex!"
                    else:
                        self.__score += 4
                else:
                    print "regex missing for: ", f.name, key, f.size
            else:
                # Check these exist at least
                print "Found extraneous file: ", f.name

        if all_good:
            self.__score += 4

    def __check_user(self):
        reg = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*?$')
        file_info = self.__tar.getmember('hunt/USER')
        if file_info.size > 1 and file_info.isfile():
            fp = self.__tar.extractfile(file_info)
            self.__user = fp.read().strip()
            fp.close()

        else:
            self.__user = ''
        if reg.match(self.__user) is not None:
            self.__score += 4
        else:
            print "Username seems invalid?"

    def __check_name(self):
        reg = re.compile(r'^[a-zA-Z, ]+?$')
        file_info = self.__tar.getmember('hunt/MYNAME')
        if file_info.size > 1 and file_info.isfile():
            fp = self.__tar.extractfile(file_info)
            self.__name = fp.read().strip()
            fp.close()
        else:
            self.__name = ''
        if reg.match(self.__name) is not None:
            self.__score += 4
        else:
            print "Full Name seems invalid?"

    def __check_submit(self):
        submit_hash = 'f5a56cf19b5c2631dd6c6c81f597989f'
        submit_size = 1554

        file_info = self.__tar.getmember('hunt/submit.sh')
        fp = self.__tar.extractfile(file_info)
        file_hash = md5(fp.read()).hexdigest()
        fp.close()

        if file_info.size == submit_size and file_hash == submit_hash:
            self.__score += 40

    def __check_file_sets(self):
        all_files = set(ALL)
        theirs = set(self.__map.values())

        return all_files.issubset(theirs)

    def grade(self):
        self.__check_submit()
        self.__check_user()
        self.__check_name()
        self.__check_all_files()

        print "Score for %s: %d" % (self.__user, self.__score)

if __name__ == '__main__':

    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print "Usage:"
        print "%s TARFILE" % sys.argv[0]
        print "Where:"
        print "TARFILE  - Tarfile submitted to be graded."
        sys.exit(1)

    sub = Submission(sys.argv[1])
    sub.grade()
