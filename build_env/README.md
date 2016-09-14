README
======

- Requires a wordlist file
  
  - You can find one somewhere on the internet or, there may be one in
    /usr/share/dict/words on some systems.

- First, generate a random wordlist from a source one using `make_random_word_list.sh`

- Next, randomly pick some number of words from the random word list you made using
  `pick_N_random_random_Words.sh`

- Now you have a randomly chosen fixed size set of words to use as input to generate
  a completely random file system hierarchy layout from. Words from the list of
  randomly chosen names will be, yes randomly, chosen to be used as file or directory
  names.

- Next, run `gen_fs_hierarchy.py` given the fixed size list of random words. This will
  output shell commands to run to generate a randomized filesystem hierarchy with
  relatively random numbers of files and directories with relatively random hierarchy
  depths.
