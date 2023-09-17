#!/usr/bin/perl
use strict;
use warnings;
my $map =[];
open my $fh, "input5_lines.txt";
while (my $line = <$fh>) {
  my ($start,$end) = split("->",$line);
  my ($col1,$row1) = split(",",$start);
  my ($col2,$row2) = split(",",$end);

  if ($row1 != $row2 && $col1 != $col2) {
    my $dirx = $row1 > $row2 ? -1 : 1;
    my $diry = $col1 > $col2 ? -1 : 1;
    for my $i (0..abs($row1-$row2)) {
      $map->[$row1+$i*$dirx][$col1+$i*$diry]++;
    }
  }

  elsif ($row1 == $row2 && $col1 == $col2) {
    $map->[$row1][$col1]++;
  }
  elsif ($row1 != $row2) {
    for my $i (min($row1,$row2) .. max($row1,$row2)) {
      $map->[$i][$col1]++;
    }
  }
  else {
    for my $i (min($col1,$col2) .. max($col1,$col2)) {
      $map->[$row1][$i]++;
    }
  }
#  print "\n",$line,"\n";
#  print_test_map($map);
}

my $total = 0;
foreach my $row (@$map) {
  foreach my $col (@$row) {
    $col = 0 unless $col;
    $total++ if $col > 1;
  }
}
print "Total: $total\n";

sub abs {
  my $a = shift;
  return -1*$a if $a < 0;
  return $a;
}
sub min {
  my $a = shift;
  my $b = shift;
  return $a if $a < $b;
  return $b;
}

sub max {
  my $a = shift;
  my $b = shift;
  return $a if $a > $b;
  return $b;
}

sub print_test_map {
  my $map = shift;
  foreach my $i (0..9) {
    foreach my $j (0..9) {
      my $sym = $map->[$i][$j];
      $sym = "." unless $sym;
      print "$sym ";
    }
    print "\n";
  }
}
__DATA__
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
