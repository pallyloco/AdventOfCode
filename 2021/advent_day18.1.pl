#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

my $sum = "";
open my $fh, "input_day18.txt" or die;
while ( my $line = <$fh> ) {
    $line =~ s/\s+//g;
    last unless $line;
    my $done = 0;
    $sum = "[$sum,$line]" if $sum;
    $sum = $line unless $sum;
    print "\n$sum\n";

    #my $x = <>;
    while ( not $done ) {

        #print "\n$sum\n";
        $done = 0;
        my $new_sum = reduce($sum);
        $done = $sum eq $new_sum;
        $sum = $new_sum;
    }

    print "$sum\n";
}
print sum($sum),"\n";

sub reduce {
    my $string = shift;

    my ( $split_left, $split_number, $split_right );
    my (
         $explode_left,  $left_number, $right_number,
         $explode_right, $basic_node
    );

    # search for something that needs exploding
    my $open  = 0;
    my @chars = split "", $string;
    $explode_left = $string;
    $basic_node   = "";
    foreach my $i ( 0 .. length($string) - 1 ) {
        $open++ if $chars[$i] eq '[';
        $open-- if $chars[$i] eq ']';

        # needs expanding, find first pair that matches
        if ( $open > 4 && $chars[$i] eq '[' ) {
            $explode_right = join "", @chars[ $i .. length($string) - 1 ];
            $explode_left  = join "", @chars[ 0 .. $i - 1 ];
            if ( $explode_right =~ /^(\[(\d+),(\d+)\])/ ) {
                $basic_node   = $1;
                $left_number  = $2;
                $right_number = $3;
                $explode_right =~ s/^\[\d+,\d+\]//;
                last;
            }
        }
    }

    ########## do the explosions before splits ############
    if ($basic_node) {

        #print "$explode_left   >>$basic_node<<   $explode_right\n";

        # find the closest number to this node
        if ( $explode_right =~ /(\d+).*?$/ ) {
            my $new = $1 + $right_number;
            $explode_right =~ s/(\d+)(.*?)$/$new$2/;
        }

        # find the closest number to this node
        if ( $explode_left =~ /^.*[^\d](\d+)/ ) {
            my $new = $1 + $left_number;
            $explode_left =~ s/^(.*[^\d])(\d+)/$1$new/;
        }

        # make new node
        return $explode_left . "0" . $explode_right;

    }

    ########## do splits ############
    $split_left = $string;
    if ( $string =~ /^(.*?)(\d\d+)(.*)$/ ) {
        ( $split_left, $split_number, $split_right ) = ( $1, $2, $3 );

        #print "$split_left   >>$split_number<<   $split_right \n";
        my $floor = int( $split_number / 2 );
        my $ceil  = int( $split_number / 2 + 0.5 );
        return $split_left . "[$floor,$ceil]" . $split_right;
    }
    return $string;

}

sub sum {
    my $string = shift;
    while ( $string =~ /^(.*?)(\[\d+,\d+\])(.*)$/ ) {
        my ( $left, $node, $right ) = ( $1, $2, $3 );
        my ($n1,$n2) = ($node=~/(\d+),(\d+)/);
        my $sum = 3*$n1 + 2* $n2;
        $string = $left . $sum . $right;
    }
    return $string;

}

__DATA__
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]