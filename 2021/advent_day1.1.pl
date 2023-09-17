#!/usr/bin/perl
use strict;
use warnings;
open my $fh, "input.txt";
my $last;
my $up;
while (my $line = <$fh>) {
  chomp $line;
  $last = $line unless defined $last;
  if ($line > $last) {
    $up++;
  }
  $last = $line;
}
print ("$up");
