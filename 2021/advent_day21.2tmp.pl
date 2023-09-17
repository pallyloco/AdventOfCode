#!/usr/bin/perl
use strict;
use warnings;

my $max_score = 5;

# ======================================================================
# get user input
# ======================================================================

open my $fh, "input_day21.txt" or die;
my @lines = <DATA>;
my @positions;
my @scores = ( 0, 0 );
my @wins   = ( 0, 0 );
my @losses = ( 0, 0 );

foreach my $player ( 0 .. 1 ) {
    ( $positions[$player] ) = ( $lines[$player] =~ /:\s+(\d+)/ );
    $positions[$player]--;
}

# ======================================================================
# All possible totals for rolling 3x with a dice that only has 3 faces
# ======================================================================
my @possible_combinations = (
                              1 + 1 + 1, 1 + 1 + 2, 1 + 1 + 3, 1 + 2 + 1,
                              1 + 2 + 2, 1 + 2 + 3, 1 + 3 + 1, 1 + 3 + 2,
                              1 + 3 + 3, 2 + 1 + 1, 2 + 1 + 2, 2 + 1 + 3,
                              2 + 2 + 1, 2 + 2 + 2, 2 + 2 + 3, 2 + 3 + 1,
                              2 + 3 + 2, 2 + 3 + 3, 3 + 1 + 1, 3 + 1 + 2,
                              3 + 1 + 3, 3 + 2 + 1, 3 + 2 + 2, 3 + 2 + 3,
                              3 + 3 + 1, 3 + 3 + 2, 3 + 3 + 3,
);

# ======================================================================
# foreach position on the board, what is the new position
# ======================================================================
my %combos;
foreach my $combo (@possible_combinations) {
    $combos{$combo}++;
}

my @pos_array;
foreach my $combo ( keys %combos ) {
    foreach my $position ( 0 .. 9 ) {
        $pos_array[$combo][$position] = ( $position + $combo ) % 10;
    }
}

# ======================================================================
# play the game
# ======================================================================
play_game( 0, \@positions, \@scores );

sub play_game {
    my $player       = shift || 0;
    my $positions    = shift;
    my $scores       = shift || [ 0, 0 ];
    my $move         = shift || 0;
    my $combinations = shift || 1;
    my $moves        = shift || "";
    my $factor       = $combos{$move};

    if ( $scores[$player] >= $max_score ) {
        $wins[$player] += $factor * $combinations;
        print "Player $player won\n";
    }
    else {
        my @new_position = @$positions;
        my @new_scores   = @$scores;
        if ($move) {
            print "P:$player, M: $moves, N: $move, ";
            $new_position[$player] = $pos_array[$move][ $positions[$player] ];
            $new_scores[$player] =
              $scores[$player] + $new_position[$player] + 1;
            print "S: ", $new_scores[$player], "\n";
        }
        my $new_player = ( $player + 1 ) % 2;

        foreach my $combo ( sort keys %combos ) {
            play_game( $new_player, \@new_position, \@new_scores, $combo,
                       $combinations * $factor,
                       $moves . $combo );
        }
    }

}

__DATA__
Player 1 starting position: 4
Player 2 starting position: 8
