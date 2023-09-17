#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_lanternfish.txt" or die;
my $data = <$fh>;
my @fishes = split(",",$data);

foreach my $day (1..80) {
  my @new;
  foreach my $fish (@fishes) {
    $fish--;
    if ($fish < 0) {
      push @new,8;
      $fish = 6;
    }
  }
  push @fishes,@new;
}
print (scalar(@fishes),"\n");
__DATA__
3,4,3,1,2
