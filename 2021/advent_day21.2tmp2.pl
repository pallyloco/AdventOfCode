#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_day21.txt" or die;
my @lines = <DATA>;
my @positions;
foreach my $player ( 0 .. 1 ) {
    ( $positions[$player] ) = ( $lines[$player] =~ /:\s+(\d+)/ );
    $positions[$player]--;
}

my $max_score = 8;

my @won = ( 0, 0 );

my @possible_combinations = (
                              1 + 1 + 1, 1 + 1 + 2, 1 + 1 + 3, 1 + 2 + 1,
                              1 + 2 + 2, 1 + 2 + 3, 1 + 3 + 1, 1 + 3 + 2,
                              1 + 3 + 3, 2 + 1 + 1, 2 + 1 + 2, 2 + 1 + 3,
                              2 + 2 + 1, 2 + 2 + 2, 2 + 2 + 3, 2 + 3 + 1,
                              2 + 3 + 2, 3 + 3 + 3, 3 + 1 + 1, 3 + 1 + 2,
                              3 + 1 + 3, 3 + 2 + 1, 3 + 2 + 2, 3 + 2 + 3,
                              3 + 3 + 1, 3 + 3 + 2, 3 + 3 + 3,
);

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
my @player_one;
my @player_two;
possible_wins( 0, 3, '', \@player_one );
possible_wins( 0, 7, '', \@player_two );
use Data::Dumper;
print Dumper \@player_one,\@player_two;die;

foreach my $result (@player_one) {
    my @moves = split ",", $result->{-moves};
    shift @moves;
    $result->{-array} = \@moves;
    my $likelyhood = 1;
    $result->{-num_moves} = scalar(@moves);
    foreach my $move (@moves) {
        $likelyhood = $likelyhood * $combos{$move};
    }
    $result->{-likely} =$likelyhood;
    $result->{-winner} = scalar (@moves)%2;
}

foreach my $result (@player_two) {
    my @moves = split ",", $result->{-moves};
    shift @moves;
    $result->{-array} = \@moves;
    $result->{-num_moves} = scalar(@moves);
    my $likelyhood = 1;
    foreach my $move (@moves) {
        if (not defined $combos{$move}) {
            my $x = 1;
        }
        $likelyhood = $likelyhood * $combos{$move};
    }
    $result->{-likely} =$likelyhood;
    $result->{-winner} = scalar (@moves)%2 + 1;
}


# player one
my $total = 1;
foreach my $result (@player_one) {
    my $moves = $result->{-array};
    if ( $result->{-winner} == 0 ) {
        
        foreach my $result2 (@player_two) {
            $total += $result2->{-likely} if $result2->{-winner}==1 && $result2->{-num_moves} > $result->{-num_moves};            
            $total *= $result->{-likely}
        }        
        
    }
}
print $total, "\n";

sub possible_wins {
    my $score      = shift;
    my $position   = shift;
    my $prev_moves = shift;
    my $result     = shift;
    $position = $position % 10;
    if ( $score > $max_score ) {
        print $score, ", ", $prev_moves, ", ", length($prev_moves), "\n";
        push @$result, { -moves => $prev_moves, -score => $score };
        return;
    }
    foreach my $combo ( keys %combos ) {
        my $new_score = possible_wins(
                             $score + 1 + ($position + $pos_array[$combo][$position]%10),
                             $position + $pos_array[$combo][$position],
                             $prev_moves . ",$combo",
                             $result,
        );
    }
}

die;

my $output_num = 1 << 21;

play_game( 0, $positions[0], 0, $positions[1], 0 );
print "@won\n";

sub play_game {
    my $player    = shift;
    my $position0 = shift;
    my $score0    = shift;
    my $position1 = shift;
    my $score1    = shift;

    my $game_over = 0;

    if ( $player == 0 ) {
        foreach my $combo (@possible_combinations) {
            my $new_pos   = $pos_array[$combo][$position0];
            my $new_score = $score0 + $new_pos + 1;
            if ( $new_score >= $max_score ) {
                $won[0]++;
                print "@won\n" unless ( $won[0] + $won[1] ) % $output_num;
                $game_over = 1;
            }
            if ( not $game_over ) {
                play_game( 1, $new_pos, $new_score, $position1, $score1 );
            }
        }
    }
    else {
        foreach my $combo (@possible_combinations) {
            my $new_pos   = $pos_array[$combo][$position1];
            my $new_score = $score1 + $position1 + 1;
            if ( $new_score >= $max_score ) {
                $won[1]++;
                print "@won\n" unless ( $won[0] + $won[1] ) % $output_num;
                $game_over = 1;
            }
            if ( not $game_over ) {
                play_game( 0, $position0, $score0, $new_pos, $new_score );
            }
        }
    }
}
__DATA__
Player 1 starting position: 4
Player 2 starting position: 8
