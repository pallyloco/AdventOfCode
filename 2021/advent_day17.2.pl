#!/usr/bin/perl;
use strict;
use warnings;

# ===============================================================
# get data
# ===============================================================
open my $fh, 'input_day17.txt' or die;
my $line = <$fh>;
my ( $x1, $x2, $y1, $y2 ) =
  ( $line =~ /x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)/ );
if ( $x1 > $x2 ) { ( $x1, $x2 ) = reverse( $x1, $x2 ); }
if ( $y1 > $y2 ) { ( $y1, $y2 ) = reverse( $y1, $y2 ); }

my @target_limits = ( COORD->new( $y1, $x1 ), COORD->new( $y2, $x2 ) );

# ===============================================================
# puzzle
# ===============================================================

# calculate the minimum and maximum x velocity
my $min_x_velocity =
  int( ( -1 + sqrt( 1 + 8 * $target_limits[0]->col ) ) / 2 + 0.9999999999 );
my $max_x_velocity = int( $target_limits[1]->col + 1 );
my $max_y_velocity = -$target_limits[0]->row - 1;
my $min_y_velocity = $target_limits[0]->row - 1;

print "initial velocities: $min_x_velocity,$max_y_velocity\n";

my $total_hits = 0;
foreach my $vx ( $min_x_velocity - 1 .. $max_x_velocity + 1 ) {
    foreach my $vy ( $min_y_velocity .. $max_y_velocity ) {
        my $hit = throw( $vx, $vy, \@target_limits );
        if ($hit) {
            $total_hits++;
        }
    }
}
print "Total hits $total_hits\n";

# ===============================================================
# throw
# ===============================================================
sub throw {
    my $vx     = shift;
    my $vy     = shift;
    my $target = shift;
    my $x      = 0;
    my $y      = 0;
    while (1) {
        $x = $x + $vx;
        $y = $y + $vy;
        if ( $x >= $target->[0]->col && $x <= $target->[1]->col ) {
            if ( $y >= $target->[0]->row && $y <= $target->[1]->row ) {
                return 1;
            }
        }
        last if $y < $target->[0]->row;
        if ( $vx != 0 ) {
            $vx = $vx < 0 ? $vx + 1 : $vx - 1;
        }
        $vy = $vy - 1;

    }
    return 0;
}

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

package main;

__DATA__
target area: x=20..30, y=-10..-5
