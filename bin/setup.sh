#!/bin/bash

# Create password file
# and put password in it
mkdir -p ~/.shutit/mortgagecomparison

touch ~/.shutit/mortgagecomparison/gitusername
chmod 600 ~/.shutit/mortgagecomparison/gitusername
echo "Input username for git repo"
read u
echo -n $u > ~/.shutit/mortgagecomparison/gitusername

touch ~/.shutit/mortgagecomparison/gitpass
chmod 600 ~/.shutit/mortgagecomparison/gitpass
echo "Input password for git repo"
read p
echo -n $p > ~/.shutit/mortgagecomparison/gitpass
