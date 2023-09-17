#!/usr/bin/perl
use strict;
use warnings;

my $depth = 0;
my $horiz = 0;

open my $fh, "input2.txt";
while (my $line = <$fh>){
  my ($cmd,$amt) = split " ",$line;
  if ($cmd eq 'forward') {
    $horiz = $horiz + $amt;
  }
  elsif ($cmd eq 'down') {
    $depth = $depth + $amt;
  }
  elsif ($cmd eq 'up') {
    $depth = $depth - $amt;
  }
  else {
    die "ERROR: $line\n";
  }
}
print "depth: $depth, horiz: $horiz\n";
print $depth * $horiz,"\n";
