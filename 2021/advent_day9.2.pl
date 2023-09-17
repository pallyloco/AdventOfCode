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
my %lowpoints;
my @sizes;

foreach my $x (0..$width-1) {
  foreach my $y (0..$height-1) {
    my $lowpoint = is_low($x,$y,$width,$height,\@map);
    if ($lowpoint) {
      $lowpoints{$y,",",$x}++;
    }
  }
}

foreach my $row (0..$height-1) {
 foreach my $col (0..$width-1) {
     next if $map[$row][$col] eq ' ';
     next if $map[$row][$col]==9;
     my $size = calculate_size($row,$col,$width,$height,\@map);
     print_map($width,$height,\@map);
     print "$size\n";
     push @sizes,$size;
   }
 }
@sizes = sort {$b<=>$a} @sizes;
print "\n\nANSWER: ",$sizes[0]*$sizes[1]*$sizes[2],"\n";
print "Number of basins: ",scalar(@sizes),"\n";

sub print_map {
  my $width = shift;
  my $height = shift;
  my $map = shift;

  print "\n\n";
  foreach my $row (0..$height-1) {
    foreach my $col (0..$width-1) {
        if (exists $lowpoints{$row,",",$col}) {
          print (".");
        }
        else {
          print $map->[$row][$col];
        }
    }
    print "\n";
  }
}

sub calculate_size {
  my $row = shift;
  my $col = shift;
  my $width = shift;
  my $height = shift;
  my $map = shift;
  my $size = shift || 0;

  my $c = $col;
  while ($c > -1 && $map[$row][$c] ne ' ' && $map->[$row][$c] != 9) {
    $c--;
  }
  $c++;
  while ($c < $width && $map[$row][$c] ne ' ' && $map->[$row][$c] != 9) {
    $size++;
    $map->[$row][$c] = ' ';
    if ($row+1 < $height && $map[$row+1][$c] ne ' '
        && $map[$row+1][$c] != 9) {
          $size = calculate_size($row+1,$c,$width,$height,$map,$size);
    }
    if ($row-1 > -1 && $map[$row-1][$c] ne ' '
        && $map[$row-1][$c] != 9) {
          $size = calculate_size($row-1,$c,$width,$height,$map,$size);
    }
    $c++;
  }
  return $size;
}

sub is_low {
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
