#!/usr/bin/perl
use strict;
use warnings;

open my $fh, 'input_day20.txt' or die;

# read code
my @decode;
while ( my $line = <$fh> ) {
    chomp $line;
    $line =~ s/\#/1/g;
    $line =~ s/\./0/g;
    push @decode, split "", $line;
    last if $line =~ /^\s*$/;
}
print "read code\n";

# read pic
my @pic;
while ( my $line = <$fh> ) {
    $line =~ s/\#/1/g;
    $line =~ s/\./0/g;
    chomp $line;
    push @pic, [ split "", $line ];
        last if $line =~ /^\s*$/;
    
}
print "read pic\n";
my $pic = MAP->new( \@pic );
    $pic->border(10,'0');
    $pic->print;


# enhance image twice
foreach my $i ( 0 .. 1 ) {
    my @enhanced_image;
    foreach my $coord ($pic->coords) {
        my $sq = $pic->semi_square($coord);
        my @code;
        foreach my $sq_coord ($sq->coords) {
            push @code,$sq->value($sq_coord);
        }
        my $number = BtoD->decimal(\@code);
        $enhanced_image[$coord->row][$coord->col] = $decode[$number];
    }
    $pic = MAP->new(\@enhanced_image);
    print "\n\n";
    $pic->print;
}

# number of lit cells
my $lit_cells = 0;
foreach my $coord ($pic->coords) {
    next if $coord->row == 0;
    next if $coord->row == $pic->height;
    next if $coord->col == 0;
    next if $coord->col == $pic->width;
    $lit_cells += $pic->value($coord);
}
print "\nANSWER: $lit_cells\n";

# ===============================================================
package COORD;
# ===============================================================
sub new {
    my $class = shift;
    my $row   = shift;
    my $col   = shift;
    return bless { -row => $row, -col => $col };
}

sub row {
    my $self = shift;
    return $self->{-row};
}

sub col {
    my $self = shift;
    return $self->{-col};
}

sub neighbours {
    my $self   = shift;
    my $height = shift;
    my $width  = shift;

    my $row = $self->row;
    my $col = $self->col;
    my @n;
    push @n, COORD->new( $row - 1, $col )     unless $row - 1 < 0;
    push @n, COORD->new( $row + 1, $col )     unless $row + 1 > $height;
    push @n, COORD->new( $row,     $col - 1 ) unless $col - 1 < 0;
    push @n, COORD->new( $row,     $col + 1 ) unless $col + 1 > $width;
    return \@n;
}

# ===============================================================
package MAP;
# ===============================================================
sub new {
    my $class = shift;
    my $map   = shift;
    
    return bless { -map => $map };
}

sub coords {
    my $self = shift;
    my @coords;
    foreach my $row (0..$self->height) {
        foreach my $col (0..$self->width) {
            push @coords,COORD->new($row,$col); 
        }
    }
    return @coords;       
}
sub border {
    my $self = shift;
    my $size = shift;
    my $value = shift;
    my @coords = $self->coords;
    
   my @new_map;
    foreach my $row (0..$self->height + 2*$size) {
        foreach my $col (0.. $self->width + 2*$size) {
            $new_map[$row][$col] = $value;
        }
    }
    foreach my $coord (@coords) {
        $new_map[$coord->row+$size][$coord->col+$size] = $self->value($coord);
    }
    $self->map(\@new_map);
}
    

sub semi_square {
    my $self  = shift;
    my $coord = shift;
    my $size  = shift || 1;
    my @n;
    foreach my $row ( $coord->row - $size .. $coord->row + $size ) {
        my @tmp;
        foreach my $col ( $coord->col - $size .. $coord->col + $size )
        {
            if (    $col < 0
                 || $col > $self->width
                 || $row < 0
                 || $row > $self->height )
            {
                push @tmp, 0;
            }
            else { push @tmp, $self->value(COORD->new($row,$col)); }
        }
        push @n, \@tmp;
    }
    return MAP->new(\@n);
}

sub value {
    my $self  = shift;
    my $coord = shift;
    $self->map->[ $coord->row ][ $coord->col ] = shift if @_;
    return $self->map->[ $coord->row ][ $coord->col ];
}

sub map {
    my $self = shift;
    $self->{-map} = shift if @_;
    return $self->{-map};
}

sub height {
    my $self = shift;
    $self->{-height} = scalar(@{$self->map}) - 1;
    return $self->{-height};
}

sub width {
    my $self = shift;
    $self->{-width} = scalar(@{$self->map->[0]}) - 1;
    return $self->{-width};
}

sub print {
    my $self    = shift;
    my $spacing = shift || 1;
    my $height  = $self->height || 9;
    my $width   = $self->width || 9;
    foreach my $row ( 0 .. $height ) {
        foreach my $col ( 0 .. $width ) {
            my $coord = COORD->new( $row, $col );
            my $value = $self->value($coord);
            $value = "." unless defined $value;
            if ( length($value) < $spacing ) {
                $value = " " x ( $spacing - length($value) ) . $value;
            }
            print $value;
        }
        print "\n";
    }
}

# ==============================================================================
# binary to decimal
# ==============================================================================
package BtoD;

sub decimal {
    my $class  = shift;
    my $bits   = shift;
    my $number = 0;
    while (@$bits) {
        my $bit = shift @$bits;
        $number = $number * 2 + $bit;
    }
    return $number;
}


package main;

__DATA__
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###