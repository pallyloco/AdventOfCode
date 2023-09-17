#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_day21.txt" or die;
my @lines = <DATA>;
my @scores;
my @positions;
foreach my $player ( 0 .. 1 ) {
    ( $positions[$player] ) = ( $lines[$player] =~ /:\s+(\d+)/ );
    $scores[$player] = 0;
    $positions[$player]--;
}

my $die       = 0;
my $max_score = 21;
my $die_roll  = 0;

my $game_over = 0;

my ($score0,$score1) = play_game($positions[0], $scores[0],$positions[1], $scores[1],
0);
print "$score0, $score1\n";


sub play_game {
    my $position0 = shift;
    my $score0    = shift;
    my $position1 = shift;
    my $score1    = shift;
    my $die_roll  = shift;

    if ( $die_roll % 6 < 3 ) {
        my $die = $die_roll%100+1;
        $die_roll++;
        ( $position0, $score0 ) = roll_die( $die, $die_roll, $position0, $score0 );
    }
    else {
        my $die = $die_roll%100+1;
        $die_roll++;
        ( $position1, $score1 ) = roll_die( $die, $die_roll, $position1, $score1 );
    }
    $game_over = $score0 >= $max_score || $score1 >= $max_score; 
    return ($score0,$score1) if $game_over;
    return play_game($position0,$score0,$position1,$score1,$die_roll);
}

sub roll_die {
    my $roll       = shift;
    my $which_roll = shift;
    my $position   = shift;
    my $score      = shift;
    $position = ( $position + $roll ) % 10;

    $score += $position + 1 unless $which_roll % 3;
    return ( $position, $score );
}

__DATA__
Player 1 starting position: 4
Player 2 starting position: 8
