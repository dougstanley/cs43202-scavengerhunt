# Command Line Scavenger Hunt!!1!11!!!one!!!1!

For this scavenger hunt, we'll be logging into the departmental servers
wasp and hornet. It doesn't matter which one you log into, just choose
one.

## Warmup - Working the shell

Lets start with a few warm ups before the real work begins.

### Getting Help

Remember, you always can use man to get info on available commands (and I can
guarantee you, you will be doing this).

Start by looking at the man page for man itself:

```bash
man man
```

Also, there is help for some of the `bash` builtins, try typing:

```bash
help
help help
help echo
```

### bash builtins

There's plenty of stuff built right into bash. For example, we can output
text to stdout. We can also output values of variables. Try:

```bash
echo Hello World!
echo "Hello $USER"
```

### Pipes and Redirection

Remember, you can redirect the output of one command to the input of another
command by putting a `|` in between, i.e.:

```bash
echo "TEST" | tr EST est
```

You can also take the output of a command and redirect it to a file with
`>` to overwrite file, or `>>` to just append to the file, i.e.

```bash
echo TEST > foo
```

You can run a command an replace it's standard input with the content of
a file instead with `<`, i.e.

```bash
cat < foo
```

### Put it all together

```bash
echo IT WORKED
echo IT WORKED >> ~/public_html/test.txt
ls -l ~/public_html/test.txt
chmod +r ~/public_html/test.txt
ls -l ~/public_html/test.txt
chmod a+r ~/public_html/test.txt
ls -l ~/public_html/test.txt
```

## The Set Up

Before you begin the hunt, you need a few things set up. If you don't follow
these steps in detail, or try to skip any, you will likely not pass. So,
just follow along step by step, don't try to improvise at this point.

1. You need a directory to store the things you find which you will later
   submit.
  * After this, you will have a directory in your home directory called hunt.
    `~` is an alias/shortcut for the full path to your home directory.
  * The second command, `chmod`, set the permissions on that directory so
    that you and only you have full permissions on that directory (read,write
    and execute, which for directories, execute means that you can enter that
    directory), and everyone else, has no permissions at all. The leading zero
    basically disables special permissions that we'll cover later.


```bash
mkdir ~/hunt
chmod 0700 ~/hunt
```

2. Now that you have a hunt directory, you need to make sure your public_html
   directory is set up. This is how you will publish your end results, by
   making them downloadable. You will also need to adjust the permissions on
   the public_html folder, as well as your home directory. We'll adjust all
   the permissions to best practices recomendations.

```bash
mkdir -p ~/public_html
chmod 0701 ~/
chmod 0701 ~/public_html
```

3. Now we can check to see if it worked. Lets create a test file and then
   try to access it from the internet.

```bash
echo "IT WORKED!!" > ~/public_html/test123.txt
chmod 0644 ~/public_html/test123.txt
```

4. Now try and access http://web.cs.kent.edu/~USERNAME/test123.txt
   * Make sure to substitute *YOUR* username on wasp (i.e. your flashline
     username) where you see the text `USERNAME` above!
   * If you see "IT WORKED!!", then congrats, you're done with the set up,
     and you can now begin the scavenger hunt!
   * If you do NOT see the text, something didn't go right, re-visit all the
     previous steps and make sure you do them all. If it's still not working,
     ASK FOR HELP! Send me an email!


## The hunt is on!

During the scavenger hunt, you will be finding clues hidden in various
locations on the departmental servers. The first clue is bellow. Find the
first clue, and it should lead you to finding the next, etc. Along the way,
you will be collecting things into a directory of your own that you will
submit to me at the end (this is what gets graded, and it will be
automatically graded, so follow directions closely).

To begin, start by navigating to *MY* hunt directory:

```bash
cd ~dmstanle/hunt
```

Verify that you are in the correct directory by typing `pwd` and you
should see `/users/kent/dmstanle/hunt`.

Now that you're in the correct starting directory, begin by navigating
around the hierarchy using the `ls` and `cd` commands. Use `ls` to see
what the contents of the directories are. Navigate to the various directories
and keep using `ls` to see what files exist.

The first clue is in a file named **tacocat**! Once you find the directory
that is holding the **tacocat** file, read the next clue by typing:

```bash
cat tacocat
```

That clue will give you directions to find the next clue, which will lead
to the next, so on and so forth. Make sure to follow every direction contained
in the various clues. Also, every clue you find, copy the file containing it
to your own hunt directory! For example, from inside the directory containing
the first clue (the tacocat file), copy it to your hunt directory with:

```bash
cp tacocat ~/hunt
```

The final clue will tell you how to properly submit your scavenger hunt.

***GOOD LUCK***
