#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_day21.txt" or die;
my @lines = <$fh>;
my @scores;
my @positions;
foreach my $player (0 ..1) {
    ($positions[$player]) = ($lines[$player] =~ /:\s+(\d+)/);
    $scores[$player] = 0;
    $positions[$player]--;
}

my $die = 0;
my $max_score = 1000;
my $die_rolls = 0;
while (1) {
    
    foreach my $roll (1..3) {    
        $die++;
        $die = $die%100;
        $positions[0] += $die;
        $die_rolls++;
    }
    $scores[0] += $positions[0]%10+1;
    print "Player 1: $scores[0]\n";
    last if $scores[0]>=$max_score;
    
    
    foreach my $roll (1..3) {    
        $die++;
        $die = ($die)%100;
        $positions[1] += $die;
        $die_rolls++;
    }
    $scores[1] += $positions[1]%10+1;
    print "Player 2: $scores[1]\n";
    last if $scores[1]>=$max_score;

}

my $low_score = $scores[0];
$low_score = $scores[1] if $scores[1] < $scores[0];
print "DIE rolled $die_rolls times\n";
print "LOW score = $low_score\n";
print "FINAL ANSWER: ",$die_rolls*$low_score,"\n";

__DATA__
Player 1 starting position: 4
Player 2 starting position: 8