#!/usr/bin/perl
use strict;
use warnings;

my @final_bits;
open my $fh, "input_day3_1.txt";
my $counter = 0;
while (my $line = <$fh>) {
  chomp $line;
  my @bits = split "",$line;
  foreach my $i (0.. scalar(@bits)-1) {
    $final_bits[$i] += $bits[$i];
  }
  $counter++;
}

my $gamma = 0;
my $epsilon = 0;
use Data::Dumper;print Dumper $counter,\@final_bits;
foreach my $bit (@final_bits) {
  $gamma = $gamma << 1;
  $epsilon = $epsilon << 1;
  if ($bit > $counter/2) {
    $gamma = $gamma + 1;
  }
  else {
    $epsilon = $epsilon + 1;
  }
}
print "\n$gamma, $epsilon\n";
print $gamma* $epsilon,"\n";
