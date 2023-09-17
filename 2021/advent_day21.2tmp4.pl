#!/usr/bin/perl
use strict;
use warnings;

my $max_score = 21;

# ======================================================================
# get user input
# ======================================================================

open my $fh, "input_day21.txt" or die;
my @lines = <$fh>;
my @positions;
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
# find all possible combinations of win/lose for both players
# ======================================================================

my %stats =
  ( 0 => { -win => {}, -lose => {} }, 1 => { -win => {}, -lose => {} } );

foreach my $player ( 0 .. 1 ) {
    possible_wins( $player, 0, $positions[$player], '', \%stats );
}

# ======================================================================
# determine how many wins for each player
# ======================================================================

# get list of moves for each player (reverse order)
my @number_of_moves_0 = sort { $b <=> $a } keys $stats{0}{-win};
my $max_moves_player1 = $number_of_moves_0[0];

# ----------------------------------------------------------------------
# if player 1 wins with 6 moves, then player 2 lost with 5 moves
# total up all possibilities
# ----------------------------------------------------------------------

my $total_games_won = 0;
foreach my $n (@number_of_moves_0) {

    my $games_won = $stats{0}{-win}{$n};

    if ( $n > 1 ) {
        my $player_two_lost = $stats{1}{-lose}{ $n - 1 };
        $total_games_won += $games_won * $player_two_lost;
    }
    else {
        $total_games_won += $games_won;
    }

}
print "Player 1: $total_games_won\n";

# ----------------------------------------------------------------------
# if player 2 wins with 6 moves, then player 1 lost with 6 moves.
# NB: player 2 cannot win with more moves than the maximum moves
#     player 1 has played
# ----------------------------------------------------------------------
$total_games_won = 0;
foreach my $n ( keys $stats{1}{-win} ) {
    next if $n >= $max_moves_player1;
    next if $n == 0;

    my $games_won = $stats{1}{-win}{$n};

    my $player_one_lost = $stats{0}{-lose}{$n};
    $total_games_won += $games_won * $player_one_lost;
}
print "Player 2: $total_games_won\n";

# ======================================================================
# get every possible combination of wins and losses
# ======================================================================
sub possible_wins {
    my $player       = shift;
    my $score        = shift;
    my $position     = shift;
    my $prev_moves   = shift;
    my $result       = shift;
    my $combinations = shift || 1;

    $result->{$player}{$prev_moves} += $combinations;
    if ( $score >= $max_score ) {
        $result->{$player}{-win}{ length($prev_moves) } += $combinations;
        return;
    }
    elsif ( $score != 0 ) {
        $result->{$player}{-lose}{ length($prev_moves) } += $combinations;
    }

    foreach my $combo ( keys %combos ) {
        possible_wins(
                       $player,
                       $score + $pos_array[$combo][$position] + 1,
                       $pos_array[$combo][$position],
                       $prev_moves . "$combo",
                       $result,
                       $combinations * $combos{$combo},
        );
    }
}

__DATA__
Player 1 starting position: 4
Player 2 starting position: 8


