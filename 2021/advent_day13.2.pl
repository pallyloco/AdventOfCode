#!/usr/bin/perl
use strict;
use warnings;
my @map;
my $width  = 0;
my $height = 0;

open my $fh, "input_day13.txt" or die;

while ( my $line = <$fh> ) {
    chomp $line;
    last unless $line;
    my ( $col, $row ) = split( ",", $line );
    $map[$row][$col] = "*";
    $height = $row if $row > $height;
    $width  = $col if $col > $width;
}
#print_map( \@map, $width, $height );

while ( my $line = <$fh> ) {
    my ( $dir, $num ) = ( $line =~ /([xy])=(\d+)/ );
    print "dir: $dir, num $num\n";
    if ( $dir eq 'y' ) {
        $height = foldup( \@map, $num, $height, $width );
    }
    else {
        $width = foldleft( \@map, $num, $height, $width );
    }
    my $dots = 0;
    #print_map(\@map,$width,$height);
    foreach my $row ( 0 .. $height ) {
        foreach my $col (0..$width) {
            $dots++ if defined $map[$row][$col] && $map[$row][$col] eq "*";
        }
        #print "$dots\n";
    }
    #print "Dots: $dots\n";die;
}
print_map(\@map,$width,$height);

sub foldup {
    my $map    = shift;
    my $num    = shift;
    my $height = shift;
    my $width  = shift;

    my $repl_row = $num - 1;

    foreach my $row ( $num+1 .. $height ) {
        foreach my $col ( 0 .. $width ) {
            $map->[$repl_row][$col] = "*" if defined $map->[$row][$col] && $map->[$row][$col] eq "*";
         }
        $repl_row--;
    }
    $height = $num-1;
}

sub foldleft {
    my $map    = shift;
    my $num    = shift;
    my $height = shift;
    my $width  = shift;

    my $repl_col = $num - 1;

    foreach my $col ( $num+1 .. $width ) {
        foreach my $row ( 0 .. $height ) {
            $map->[$row][$repl_col] = "*" if defined $map->[$row][$col] && $map->[$row][$col] eq "*";
        }
        $repl_col--;
    }
    $height = $num-1;
     



}

sub print_map {
    my $map    = shift;
    my $width  = shift;
    my $height = shift;
    print("\n");
    foreach my $row ( 0 .. $height ) {
        foreach my $col ( 0 .. $width ) {
            print "  " unless $col%5;
            $map->[$row][$col] = " " unless defined $map->[$row][$col];
            print $map->[$row][$col];
        }
        print "\n";
    }
}

__DATA__
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
