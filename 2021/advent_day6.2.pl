#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_lanternfish.txt" or die;
my $data = <$fh>;
my @tmp = split(",",$data);
my @fishes=(0,0,0,0,0,0,0,0,0);
foreach my $datum(@tmp) {
  $fishes[$datum]++;
}

foreach my $day (1..256) {
  my $new = $fishes[0];
  foreach my $i (0..7) {
    $fishes[$i] = $fishes[$i+1];
  }
  $fishes[6]+= $new;
  $fishes[8] = $new;
}
my $sum = 0;
foreach my $i (0..8) {
  $sum+=$fishes[$i];
}
print("Total: $sum\n");

__DATA__
3,4,3,1,2
