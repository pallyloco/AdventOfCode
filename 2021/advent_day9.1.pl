#!/usr/bin/perl
use strict;
use warnings;
open my $fh, "input_day9.txt" or die;

my @map = ();
foreach my $line (<$fh>) {
  chomp $line;
  push @map,[split("",$line)];
}
my $width = @{$map[0]};
my $height = @map;
my $num_lowpoints;

my $danger = 0;
foreach my $x (0..$width-1) {
  foreach my $y (0..$height-1) {
    my $lowpoint = is_low_point($x,$y,$width,$height,\@map);
    if ($lowpoint) {
      $danger += 1 + $map[$y][$x];
      $num_lowpoints++;
    }
  }
}
print "Total danger: $danger\n";
print "Number of lowpoints: $num_lowpoints\n";

sub is_low_point {
  my $col = shift;
  my $row = shift;
  my $max_col = shift;
  my $max_row = shift;
  my $map = shift;

  foreach my $drow (-1,1) {
    if ($row + $drow < $max_row && $row + $drow > -1) {
      return 0 if $map->[$row+$drow][$col] <= $map->[$row][$col];
    }
  }
  foreach my $dcol (-1,1) {
    if ($col + $dcol < $max_col && $col + $dcol > -1) {
      return 0 if $map->[$row][$col+$dcol] <= $map->[$row][$col];
    }
  }
  return 1;

}

__DATA__
2199943210
3987894921
9856789892
8767896789
9899965678
