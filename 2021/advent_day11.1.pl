#!/usr/bin/perl
use strict;
use warnings;
my $num_steps = 100;
open my $fh, "input_day11.txt" or die;

# store the data in an array
my @octopi ;
my @lines = <$fh>;
my $height = @lines - 1;
my $width;
foreach my $row (0..$height) {
  my $line = $lines[$row];
  chomp $line;
  $width = length($line) - 1;
  my @octopus = split "",$line;
  foreach my $col (0..$width) {
    $octopi[$row][$col] = $octopus[$col];
  }
}

# go over steps
my $num_flashes = 0;
foreach my $i (1..$num_steps) {
  print "\n\nNEW STEP\n";
  print_map (\@octopi, $width, $height);
  increase_energy(\@octopi,$width,$height);
  $num_flashes += go_octupuses(\@octopi,$width,$height);
}
print "\nTOTAL NUMBER OF FLASHES: $num_flashes\n";

sub increase_energy {
  my $octopi = shift;
  my $width = shift;
  my $height = shift;
  foreach my $row (0..$height) {
    foreach my $col (0..$width) {
      $octopi->[$row][$col]++;
    }
  }
}

sub go_octupuses {
  my $octopi = shift;
  my $width = shift;
  my $height = shift;
  my $increase;
  my $flashed;
  my $num_flashes = 0;
  foreach my $row (0..$height) {
    foreach my $col (0..$width) {
      $increase->[$row][$col] = 0;
      $flashed->[$row][$col] = 0;
    }
  }
  my $finished = 0;


  my $count = 0;
  while (not $finished) {
    $count++;
    print "$count> go: ";
  #  my $x = <>;

    # save increases
    foreach my $row (0..$height) {
      foreach my $col (0..$width) {
        if ($octopi->[$row][$col] > 9 && $flashed->[$row][$col] != 1 ) {
          $octopi->[$row][$col] = 0;
          $flashed->[$row][$col] = 1;
          increase_neighbours($increase,$flashed,$width,$height,$row,$col);
        }
      }
    }
    print ("\nIncreases");
    print_map ($increase, $width, $height);


    # apply increases and check if done
    $finished = 1 ;
    $num_flashes  = 0;
    foreach my $row (0..$height) {
      foreach my $col (0..$width) {
        if ($flashed->[$row][$col] == 0) {
          $octopi->[$row][$col] += $increase->[$row][$col];
        }
        else {
          $octopi->[$row][$col] = 0;
          $num_flashes++;
        }
        $finished = 0 if $octopi->[$row][$col] > 9 && $flashed->[$row][$col]==0;
        $increase->[$row][$col] = 0;
      }
    }
    print ("\nFlashed");
    print_map ($flashed, $width, $height);
    print ("\nOctopi");
    print_map ($octopi, $width, $height);
  }
  return $num_flashes;
}

sub increase_neighbours {
  my $increase = shift;
  my $flashed = shift;
  my $width = shift;
  my $height = shift;
  my $original_row = shift;
  my $original_col = shift;

  foreach my $row ($original_row-1,$original_row,$original_row+1) {
    next if $row > $height || $row < 0;
    foreach my $col ($original_col-1,$original_col,$original_col+1) {
      next if $col > $width || $col < 0;
      if ($original_row != $row || $original_col != $col ) {
        $increase->[$row][$col]++ ;
      }
    }
  }
}

sub print_map {
  my $map = shift;
  my $width = shift;
  my $height = shift;

  print "\n";
  foreach my $row (0..$height) {
    foreach my $col (0..$width) {
      print $map->[$row][$col],", ";
    }
    print "\n";
  }
}
__DATA__
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
