#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_bingo.txt" or die;

# calls
my $calls = <$fh>;
chomp $calls;
my @calls = split(",",$calls);

# boards
my @boards;
my $board = [];
while (my $line = <$fh>) {
  chomp $line;

  # new board
  unless ($line) {
    push @boards,$board if @$board;
    $board = [];
    next;
  }

  # per rows
  my @cols = split(" ",$line);
  push @$board,\@cols;
}
push @boards,$board if @$board;

close $fh;

# go over each call and check off bingo board number
foreach my $num (@calls) {
  print ("Called $num\n");
  foreach my $board (@boards) {
    foreach my $i (0..4){
      foreach my $j (0..4) {
        if ($board->[$i][$j] == $num) {
          $board->[$i][$j] = -1;
          is_board_winner($board,$num);
        }
      }
    }
  }
}

sub is_board_winner {
  my $board = shift;
  my $num = shift;

  # check rows
  my $won = 1;
  foreach my $i (0..4){
    $won = 1;
    foreach my $j (0..4) {
      if ($board->[$i][$j] != -1) {
        $won = 0;
        last;
      }
    }
    last if $won;
  }
  if ($won) {
    calculate_score($board,$num);die;
  }

  # check cols
  $won = 1;
  foreach my $i (0..4){
    $won = 1;
    foreach my $j (0..4) {
      if ($board->[$j][$i] != -1) {
        $won = 0;
        last;
      }
    }
    last if $won;
  }
  if ($won) {
    calculate_score($board,$num);die;
  }
}

sub calculate_score {
  my $board = shift;
  my $num = shift;

  my $total  = 0;
  foreach my $i (0..4){
    foreach my $j (0..4) {
      $total = $total + $board->[$i][$j] if $board->[$i][$j] > 0;
    }
  }
  use Data::Dumper;print Dumper $board;
  my $score = $num* $total;
  print "Score is $score\n";

}
