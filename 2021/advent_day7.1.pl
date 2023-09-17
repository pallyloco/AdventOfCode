#!/usr/bin/perl
use strict;
use warnings;
open my $fh, "input_day7.txt" or die;
my $line = <$fh>;
my @data = split(",",$line);
my %indices;
my $max_index =0;
foreach my $datum (@data) {
  $indices{$datum}++;
  if ($datum > $max_index) {
    $max_index = $datum;
  }
}

my $min_cost = 0;
foreach my $index (0.. $max_index) {
  my $cost = 0;
  foreach my $i (keys %indices) {
    $cost += sum(abs($i-$index))*$indices{$i};
    last if $cost > $min_cost && $min_cost;
  }
  print "$index, $cost\n";
  $min_cost = $cost unless $min_cost;
  if ($min_cost > $cost) {
    $min_cost = $cost;
  }
}

print "Final cost: $min_cost\n";

sub sum {
  my $num = shift;
  my $total = 0;
  while ($num > 0) {
    $total+= $num;
    $num--;
  }
  return $total;
}
__DATA__
16,1,2,0,4,2,7,1,2,14
