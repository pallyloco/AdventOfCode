#!/usr/bin/perl
use strict;
use warnings;


my $other_player_two_solutions = {
          '4,7' => 2,
          '6,8' => 2,
          '3,3' => 2,
          '3,9' => 2,
          '3,5' => 2,
          '8' => 3,
          '7' => 3,
          '5,6' => 2,
          '4,4' => 2,
          '3,4' => 2,
          '5,7' => 2,
          '3,8' => 2,
          '6,5' => 2,
          '4,6' => 2,
          '6,4' => 2,
          '5,3' => 2,
          '3,6' => 2,
          '6,9' => 2,
          '6,7' => 2,
          '4,5' => 2,
          '9' => 3,
          '6,3' => 2,
          '5,9' => 2,
          '4,3' => 2,
          '4,8' => 2,
          '3,7' => 2,
          '6,6' => 2,
          '5,5' => 2,
          '5,4' => 2
        };
print join "\n ",sort keys ($other_player_two_solutions);
print "\n\n";









open my $fh, "input_day21.txt" or die;
my @lines = <DATA>;
my @positions;
foreach my $player ( 0 .. 1 ) {
    ( $positions[$player] ) = ( $lines[$player] =~ /:\s+(\d+)/ );
    $positions[$player]--;
}

my $max_score = 5;

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
my @player_two_lose;
my @player_one_lose;
print "\n\nPLAYER ONE:\n";
possible_wins( 0, 3, '', \@player_one,\@player_one_lose );

print "\n\nPLAYER TWO:\n";
possible_wins( 0, 7, '', \@player_two,\@player_two_lose );
use Data::Dumper;

#print Dumper \@player_one;
#print scalar(@player_two),"\n";
#die;






foreach my $result (@player_one) {
    my @moves = split ",", $result->{-moves};
    shift @moves;
    $result->{-array}     = \@moves;
    $result->{-num_moves} = scalar(@moves);
    $result->{-winner}    = 1;
}

foreach my $result (@player_two) {
    my @moves = split ",", $result->{-moves};
    $result->{-array}     = \@moves;
    $result->{-num_moves} = scalar(@moves);
    $result->{-winner}    =  2;
}




# find redundant winners;
my $max_length2 = 0;
my $max_length1 = 0;
foreach my $result (@player_one,@player_two) {
    my $moves = $result->{-moves};
    $max_length2 = $result->{-num_moves} 
    if $result->{-num_moves} > $max_length2 && $result->{-winner} == 2;
    $max_length1 = $result->{-num_moves} 
    if $result->{-num_moves} > $max_length1 && $result->{-winner} == 1;
}
print "$max_length1, $max_length2\n";

my @tmp;
foreach my $result (@player_two) {
    my $moves = $result->{-moves};
    next if ($result->{-num_moves} > $max_length1);
    push @tmp,$result;
}
@player_two = @tmp;
print Dumper \@player_two;
print scalar(@player_two),"\n";
print scalar(@player_one),"\n";

# now, how many times did it win?
# just for now, assume that we are looking at player 1 having
# played 3x, which means player 2 does not win in two turns
foreach my $result (@player_two) {
    
}

print Dumper \@player_one;
my %stats;
foreach my $result (@player_one) {
    $stats {$result->{-num_moves}}++;
}
print Dumper \%stats;
    







die;




foreach my $result (@player_one) {
    my @moves = split ",", $result->{-moves};
    shift @moves;
    next if scalar(@moves) % 2;
    foreach my $move (@moves) {
        $result->{-array} = \@moves;
        my $likelyhood = 1;
        $result->{-num_moves} = scalar(@moves);
        foreach my $move (@moves) {
            $likelyhood = $likelyhood * $combos{$move};
        }
        $result->{-likely} = $likelyhood;
        $result->{-winner} = scalar(@moves) % 2;
    }
}

foreach my $result (@player_two) {
    my @moves = split ",", $result->{-moves};
    shift @moves;
    $result->{-array}     = \@moves;
    $result->{-num_moves} = scalar(@moves);
    my $likelyhood = 1;
    foreach my $move (@moves) {
        if ( not defined $combos{$move} ) {
            my $x = 1;
        }
        $likelyhood = $likelyhood * $combos{$move};
    }
    $result->{-likely} = $likelyhood;
    $result->{-winner} = scalar(@moves) % 2 + 1;
}

# player one
my $total = 1;
foreach my $result (@player_one) {
    my $moves = $result->{-array};
    if ( $result->{-winner} == 0 ) {

        foreach my $result2 (@player_two) {
            $total += $result2->{-likely}
              if $result2->{-winner} == 1
                  && $result2->{-num_moves} > $result->{-num_moves};
            $total *= $result->{-likely};
        }

    }
}
print $total, "\n";

sub possible_wins {
    my $score      = shift;
    my $position   = shift;
    my $prev_moves = shift;
    my $result     = shift;
    my $lost = shift;
    $position = $position % 10;
    if ( $score >= $max_score ) {
        push @$result, { -moves => $prev_moves, -score => $score };
        return;
    }
    else {
        push @$lost, { -moves => $prev_moves, -score => $score };        
    }
    foreach my $combo ( keys %combos ) {
        print "old score: ,$score, old pos: $position, roll: $prev_moves,$combo, add: ",
        $pos_array[$combo][$position]  + 1 ,
        " new score: ",$score + $pos_array[$combo][$position]  + 1 
        ."\n";
          possible_wins(
                $score + $pos_array[$combo][$position]  + 1,
                $pos_array[$combo][$position],
                $prev_moves . ",$combo",
                $result, $lost,
          );
    }
}

__DATA__
Player 1 starting position: 4
Player 2 starting position: 8
