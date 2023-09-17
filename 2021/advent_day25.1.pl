#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_day25.txt" or die;
my @lines = <$fh>;
chomp @lines;
my $max_row = @lines - 1;
my $max_col = length( $lines[0] ) - 1;

$Spot::circular = 1;
$Spot::NUM_ROWS  = $max_row + 1;
$Spot::NUM_COLS  = $max_col + 1;

# =============================================================================
# create the sea floor and add creatures to it
# =============================================================================
my $floor = Seafloor->new( $max_row, $max_col );

my @south;
my @east;

foreach my $row ( 0 .. $max_row ) {
    my @tmp = split "", $lines[$row];
    foreach my $col ( 0 .. $max_col ) {
        my $creature = Sea_cucumber->new( $tmp[$col] );
        if ($creature) {
            $floor->occupy( Spot->new( $row, $col ), $creature );
            push @south, $creature if $creature->is_south;
            push @east,  $creature if $creature->is_east;
        }
    }
}
print $floor;

# =============================================================================
# move the creatures until they get stuck
# =============================================================================
my $done = 0;
my $step = 0;
while ( not $done ) {
    my @to_move;
    $done = 1;
        $step++;
    

    foreach my $c (@east) {
        my $spot = $floor->where_is($c);
        unless ( $floor->occupied_by( $spot + $c->move_vector ) ) {
            push @to_move, [ $c, $spot + $c->move_vector ];
        }
    }
    while ( my $c = shift @to_move ) {
        $done = 0;
        $floor->move_creature(@$c);
    }

    foreach my $c (@south) {
        my $spot = $floor->where_is($c);
        push @to_move, [ $c, $spot + $c->move_vector ]
          unless $floor->occupied_by( $spot + $c->move_vector );
    }
    while ( my $c = shift @to_move ) {
        $done = 0;
        $floor->move_creature(@$c);
    }
    #if ($step%1 == 0) {
    #system 'clear';
    print "Step $step $floor";
    #}
#    <>;

}
print $floor;
print "FINAL answer $step\n";

###############################################################################
package Seafloor;
use overload '""' => "stringification";

sub new {
    my $class = shift;
    my $self = bless { -spots => {}, -creatures => {} };
    $self->height(shift);
    $self->width(shift);
    return $self;
}

sub _all_spots {
    my $self = shift;
    return $self->{-spots};
}

sub _all_creatures {
    my $self = shift;
    return $self->{-creatures};
}

sub occupy {
    my $self     = shift;
    my $spot     = shift;
    my $creature = shift;
    $self->_all_spots->{$spot}         = $creature;
    $self->_all_creatures->{$creature} = $spot;
}

sub where_is {
    my $self     = shift;
    my $creature = shift;
    return $self->_all_creatures->{$creature};
}

sub occupied_by {
    my $self = shift;
    my $spot = shift;
    return $self->_all_spots->{$spot}
      if ( $self->_all_spots && $self->_all_spots->{$spot} );
    return;
}

sub move_creature {
    my $self     = shift;
    my $creature = shift;
    my $spot     = shift;

    $self->_all_spots->{ $self->where_is($creature) } = undef;
    $self->_all_spots->{$spot}                        = $creature;
    $self->_all_creatures->{$creature}                = $spot;
}

sub height {
    my $self = shift;
    $self->{-height} = shift if @_;
    return $self->{-height};
}

sub width {
    my $self = shift;
    $self->{-width} = shift if @_;
    return $self->{-width};
}

sub stringification {
    my $self = shift;
    my $str  = "\n";
    foreach my $row ( 0 .. $self->height ) {
        foreach my $col ( 0 .. $self->width ) {
            my $c = $self->occupied_by( Spot->new( $row, $col ) );
            $str .= $c->type if $c;
            $str .= "." unless $c;
        }
        $str .= "\n";
    }
    $str .= "\n";
    return $str;
}

###############################################################################
package Sea_cucumber;

sub new {
    my $class = shift;
    my $type = shift || "";
    return unless $type eq ">" || $type eq "v";
    my $self = bless {};
    $self->type($type);
    return $self;
}

sub move_vector {
    my $self = shift;
    return Spot->new( 0, 1 ) if $self->type eq ">";
    return Spot->new( 1, 0 ) if $self->type eq "v";
}

sub type {
    my $self = shift;
    $self->{-type} = shift if @_;
    return $self->{-type};
}

sub is_south {
    my $self = shift;
    return $self->type eq "v";
}

sub is_east {
    my $self = shift;
    return $self->type eq ">";
}

###############################################################################
package Spot;
use strict;
use warnings;
our $circular;
our $NUM_ROWS;
our $NUM_COLS;

use overload "==" => "equals", '""' => "stringification", "+" => 'plus';

sub new {
    my $class = shift;
    my $row   = shift || 0;
    my $col   = shift || 0;
    my $self  = bless {};
    $self->row($row);
    $self->col($col);
    return $self;
}

sub row {
    my $self = shift;
    $self->{-row} = shift if @_;
    return $self->{-row};
}

sub col {
    my $self = shift;
    $self->{-col} = shift if @_;
    return $self->{-col};
}

sub plus {

    #   print join ", ",caller,"\n";
    #   use Data::Dumper; print "plus:\n",Dumper \@_;die;
    my $self  = shift;
    my $other = shift;
    my $row   = $self->row + $other->row;
    my $col   = $self->col + $other->col;
    if ($Spot::circular) {
        my $rows = $NUM_ROWS || 10;
        my $cols = $NUM_COLS || 10;
        $row = $row % $rows;
        $col = $col % $cols;
    }
    return Spot->new( $row, $col );
    return;
}

sub down {
    my $self = shift;
    return Spot->new( $self->row + 1, $self->col );
}

sub up {
    my $self = shift;
    return Spot->new( $self->row - 1, $self->col );
}

sub right {
    my $self = shift;
    return Spot->new( $self->row, $self->col + 1 );
}

sub left {
    my $self = shift;
    return Spot->new( $self->row, $self->col - 1 );
}

sub equals {
    my $self  = shift;
    my $other = shift;
    return $self->row == $other->row && $self->col == $other->col;
}

sub stringification {
    my $self = shift;
    return "[" . $self->row . "," . $self->col . "]";
}

package main;

__DATA__
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
