- [Setting up](#orgc51d6a9)
- [Running the app](#org158533b)
- [Roadmap <code>[3/9]</code>](#orgd4f56bf)
  - [Add argparse support](#org545300b)
  - [Pull woob configuration with account listing](#orgdef7917)
  - [Pull woob data from given woob bank backends](#orgdef6b6e)
  - [Create the converter protocol/abstract class to change from woob to beancount](#org80e6604)
  - [Read beancount data with category listing](#orgcb509ac)
  - [Allow users to interactively choose categories](#orgaa5765f)
  - [Change the tracking id method to allow merging transactions](#orge41fb17)
  - [Privacy option to hide amounts and optionally banks](#org35685e7)
  - [Find fake woob data to be able to stream](#orgd895f7f)



<a id="orgc51d6a9"></a>

# Setting up

You can use a simple direnv setup

```bash
layout python3
```

And then use the provided [Requirements file](./dev-requirements.txt) to setup an environment.

After this, you need to make a configuration file that can be read into a configuration. An example file will be given once the format stabilizes a bit. The file will be in TOML format (for readability), and read by default to the XDG location.


<a id="org158533b"></a>

# Running the app

Until a proper flit packaging is done, running the draft apps is done simply with

```bash
python -m konta
```

and dealing with the help messages

It will look for a configuration file in the common XDG path for a `konta` program, which must be a TOML file

```toml
# In ~/.config/konta/config.toml
[Default]
# Setting the category for unmatched payees.
category = "Expenses:Uncategorized"

[Accounts]
# Woob ID (from woob bank ls) to Beancount account, with a currency to be used as
# commodity for the transaction
"deadbeef0731233" = { name = "Assets:Bank:Checking", default-currency = "EUR" }

[Payees]
# An example of merging multiple payees to be the same name and the same category.
# Both 'name' and 'category' are optional here if you don't want to overwrite them.
"75 MONOP" = { name = "MONOPRIX", category = "Expenses:Food:Supermarché" }
"75 MONOPRIX" = { name = "MONOPRIX", category = "Expenses:Food:Supermarché" }

# Unused for now, but extra verifications can be done if we
# give the main input file, with valid/existing accounts.
# It takes a list of path to beancount input files
[Beans]
input = []
```


<a id="orgd4f56bf"></a>

# Roadmap <code>[3/9]</code>


<a id="org545300b"></a>

## DONE Add argparse support


<a id="orgdef7917"></a>

## DONE Pull woob configuration with account listing


<a id="orgdef6b6e"></a>

## TODO Pull woob data from given woob bank backends

Should be done by ignoring the accounts that are not in config


<a id="org80e6604"></a>

## TODO Create the converter protocol/abstract class to change from woob to beancount

The main goal here is to allow providing custom matchers from the config, probably as python modules that would be provided by the end user. Just like the first Guile version of this tool.


<a id="orgcb509ac"></a>

## DONE Read beancount data with category listing


<a id="orgaa5765f"></a>

## TODO Allow users to interactively choose categories

That entails building a module that can meaningfully interact with a Config instancea


<a id="orge41fb17"></a>

## TODO Change the tracking id method to allow merging transactions


<a id="org35685e7"></a>

## TODO Privacy option to hide amounts and optionally banks

Necessary option to be able to start streaming development, either that or the first item


<a id="orgd895f7f"></a>

## TODO Find fake woob data to be able to stream
