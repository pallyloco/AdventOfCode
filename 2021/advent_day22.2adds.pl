#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

open my $fh, "input_day22.txt" or die;

# start with a cuboid of size zero
my @boxes = ();

# ---------------------------------------------------------------------------
# Read in data
# ---------------------------------------------------------------------------
while ( my $line = <DATA> ) {
    last if $line =~ /^\s*$/;
    my ( $action, $xrange, $yrange, $zrange ) =
      ( $line =~ /^(\w+)\s+x=(.*?),y=(.*?),z=(.*?)$/ );

    # create a new cuboid
    my @coords;
    push @coords, max_min($xrange), max_min($yrange), max_min($zrange);
    my $new_box = Cuboid->new( \@coords );
    push @boxes, $new_box unless @boxes;

    print "\n\n===========\n";
    foreach my $box (@boxes) {
        print "$box\n";
    }

    # foreach box that is already there (none overlap each other)
    # compare to the new box
    my $to_add = [$new_box];
    foreach my $box (@boxes) {

        # cmp the new box with one of the original boxes
        # returns possibly more than one box
        my $to_add_later;
        foreach my $new_box (@$to_add) {
            print "\n------------------\n";
            print "Comparing $box\nwith      $new_box\n\n";

            my $t = $box->intersect($new_box);

            # keep track of all the cut-off pieces
            push @$to_add_later, @$t;
        }

        # add cut off pieces to the array in preparation for comparing
        # with one of the other non-overlapping boxes
        print "\nResults\n";
        foreach my $t (@$to_add_later) {
            print "$t\n";
        }
        $to_add = $to_add_later;
    }

    # at this point, newer boxes should not intersect with any previous
    # box.
    print "\n\n\nNEW BOX LIST\n";
    push @boxes, @$to_add if $to_add;
    foreach my $b (@boxes) {
        print "$b\n";
    }

    my $set = $action eq "on" ? 1 : 0;
}

my $total = 0;
print "\n\n\n\n";
my $i = 0;
foreach my $box (@boxes) {
    $i++;
    print "$i -> $box\n";
    $total = $total + $box->size;
}
print "FINAL ANSWER: $total\n";

sub max_min {
    my $range = shift;
    my ( $start, $end ) = ( $range =~ /(-?\d+)\.\.(-?\d+)/ );
    return ( $start, $end );
}

# ==========================================================================
# Cuboid
# ==========================================================================
package Cuboid;
use overload '""' => 'stringify';

# --------------------------------------------------------------------------
# new
# --------------------------------------------------------------------------
sub new {
    my $class = shift;
    my $coords = shift || [];
    return bless { -coords => $coords };
}

# --------------------------------------------------------------------------
# taking existing cuboid, and another cuboid
# remove part of new cube that already exists in this cube,
# ... creating new cuboids as nececarry
# returns: a set of cuboids that do not intersect with self
#
# --------------------------------------------------------------------------
sub intersect {
    my $self         = shift;
    my $other        = shift;         # cuboids
    my $good         = shift || [];
    my $needs_review = shift || [];

    # loop until no more cuts, etc to make
    while ($other) {

        # it doesn't intersect at all, keep it
        if ( $self->does_not_intersect($other) ) {
            print "no intersection $other\n";
            push @$good, $other;
            $other = undef;
            last;
        }

        # it is consumed by $self totally, ignore it
        last if $self->does_contain($other);

        # slicing and dicing, check all 6 faces
        my $changed = 0;
        foreach my $axis (qw( x y z)) {
            if ( not $changed ) {
                foreach my $side (qw (max min)) {
                    my $get_side = $axis . $side;
                    my @new = $other->slice( $axis, $side, $self->$get_side );
                    if ( scalar(@new) ) {
                        push @$good, $new[0];
                        print "Keeping $new[0]\n";
                        $other   = $new[1];
                        $changed = 1;
                        last;
                    }
                }
            }
        }
        last if not $changed;
    }
    return $good;
}

# --------------------------------------------------------------------------
# slice
# --------------------------------------------------------------------------
sub slice {
    my $self   = shift;
    my $axis   = shift;
    my $maxmin = shift;
    my $number = shift;

    my $min = $axis . "min";
    my $max = $axis . "max";

    my $non_intersecting      = $self->clone;
    my $possibly_intersecting = $self->clone;

    if ( $maxmin eq 'max' ) {
        if ( $self->$min <= $number && $number < $self->$max ) {
            $possibly_intersecting->$max($number);
            $non_intersecting->$min( $number + 1 );
            return ( $non_intersecting, $possibly_intersecting );
        }
    }

    if ( $maxmin eq 'min' ) {
        if ( $self->$min < $number && $number <= $self->$max ) {
            $non_intersecting->$max( $number - 1 );
            $possibly_intersecting->$min($number);
            return ( $non_intersecting, $possibly_intersecting );
        }
    }

    return ();

}

# --------------------------------------------------------------------------
# questions
# --------------------------------------------------------------------------

sub does_not_intersect {
    my $self  = shift;
    my $other = shift;
    return (    $self->xmax < $other->xmin
              || $self->ymax < $other->ymin
              || $self->zmax < $other->zmin )
      || (    $self->xmin > $other->xmax
           || $self->ymin > $other->ymax
           || $self->zmin > $other->zmax );
           
}

sub does_contain {
    my $self  = shift;
    my $other = shift;

    #    print "\n\n$self\n$other\n";
    #    print "does contain x ",
    #      $self->xmin <= $other->xmin && $self->xmax >= $other->xmax, "\n";
    #    print "does contain y ",
    #      $self->ymin <= $other->ymin && $self->ymax >= $other->ymax, "\n";
    #    print "does contain z ",
    #      $self->zmin <= $other->zmin && $self->zmax >= $other->zmax, "\n";
    return
         ( $self->xmin <= $other->xmin && $self->xmax >= $other->xmax )
      && ( $self->ymin <= $other->ymin && $self->ymax >= $other->ymax )
      && ( $self->zmin <= $other->zmin && $self->zmax >= $other->zmax );

}

sub is_enclosed_by {
    my $self  = shift;
    my $other = shift;
    return
         ( $self->xmin > $other->xmin && $self->xmax < $other->xmax )
      && ( $self->ymin > $other->ymin && $self->ymax < $other->ymax )
      && ( $self->zmin > $other->zmin && $self->zmax < $other->zmax );

}

# --------------------------------------------------------------------------
# housekeeping
# --------------------------------------------------------------------------

sub stringify {
    my $self = shift;
    my $s    = "[" . $self->xmin . ".." . $self->xmax . "]";
    $s .= " [" . $self->ymin . ".." . $self->ymax . "]";
    $s .= " [" . $self->zmin . ".." . $self->zmax . "]";
    $s .= "  Size: " . $self->size;
    return $s;
}

sub coords {
    my $self = shift;
    return $self->{-coords};
}

sub clone {
    my $self   = shift;
    my @coords = @{ $self->coords };
    return Cuboid->new( \@coords );
}

sub xlength {
    my $self = shift;
    return $self->xmax - $self->xmin + 1;
}

sub ylength {
    my $self = shift;
    return $self->ymax - $self->ymin + 1;
}

sub zlength {
    my $self = shift;
    return $self->zmax - $self->zmin + 1;
}

sub xmin {
    my $self = shift;
    return $self->_set_coord( 0, @_ );
}

sub _set_coord {
    my $self = shift;
    my $i    = shift;
    $self->coords->[$i] = shift if @_;
    $self->coords->[$i] = 0 unless defined $self->coords->[$i];
    return $self->coords->[$i];
}

sub xmax {
    my $self = shift;
    return $self->_set_coord( 1, @_ );
}

sub ymin {
    my $self = shift;
    return $self->_set_coord( 2, @_ );
}

sub ymax {
    my $self = shift;
    return $self->_set_coord( 3, @_ );
}

sub zmin {
    my $self = shift;
    return $self->_set_coord( 4, @_ );
}

sub zmax {
    my $self = shift;
    return $self->_set_coord( 5, @_ );
}

sub size {
    my $self = shift;
    return $self->xlength * $self->ylength * $self->zlength;
}

package main;

__DATA__
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
on x=9..11,y=9..11,z=9..11



on x=10..12,y=10..12,z=10..12
on x=9..11,y=9..11,z=9..11


==============================================================================
0)      x=10..12,   y=10..12,   z=10..12    keep
1)  +   x=11..13,   y=11..13,   z=11..13
  =>    x=13..13,   y=11..13    z=11..13    keep
  =>    x=11..12,   y=11..13    z=11..13    ... needs checking
2)      x=10..12,   y=10..12,   z=10..12    
    +   x=11..12,   y=11..13    z=11..13
  =>    x=11..12,   y=13..13    z=11..13    keep
  =>    x=11..12    y=11..12    z=11..13    ... needs checking
3)      x=10..12,   y=10..12,   z=10..12    
    +   x=11..12    y=11..12    z=11..13    
  =>    x=11..12    y=11..12    z=13..13    keep
  =>    x=11..12,   y=11..12    z=11..12    ... needs checking
4)      x=10..12,   y=10..12,   z=10..12    
    +   x=11..12,   y=11..12    z=11..12    ... is enclosed by '0', so disappears    
    
==============================================================================
After comparing 2nd box to 1st box

(1) [10..12] [10..12] [10..12]  Size: 27
(2) [13..13] [11..13] [11..13]  Size: 9
(3) [11..12] [13..13] [11..13]  Size: 6
(4) [11..12] [11..12] [13..13]  Size: 4

==============================================================================
New: x=9..11,    y=9..11,    z=9..11

on      x=10..12,   y=10..12,   z=10..12
cmp     x=9..11,    y=9..11,    z=9..11
        x=10..11    y=9..11     z=9..11          keep 9..9, 9..11,  9..11
        x=10..11    y=10..11    z=9..11          keep 10..11, 9..9, 9..11
        x=10..11    y=10..11    z=10..11         keep 10..11, 10..11, 9..9 

------------------------------------------------------------------------------
results of above
(a) [ 9.. 9] [ 9..11] [ 9..11]  Size: 9
(b) [10..11] [ 9.. 9] [ 9..11]  Size: 6
(c) [10..11] [10..11] [ 9.. 9]  Size: 4

must now cmp all of the above with box (2)  no change
(2) [13..13] [11..13] [11..13]  Size: 9
(a) [ 9.. 9] [ 9..11] [ 9..11]  Size: 9     keep [ 9.. 9] [ 9..11] [ 9..11]

(2) [13..13] [11..13] [11..13]  Size: 9
(b) [10..11] [ 9.. 9] [ 9..11]  Size: 6     keep [10..11] [ 9.. 9] [ 9..11]

(2) [13..13] [11..13] [11..13]  Size: 9
(c) [10..11] [10..11] [ 9.. 9]  Size: 4     keep [10..11] [10..11] [ 9.. 9]


must now cmp all of the above with box (3)  no change
(3) [11..12] [13..13] [11..13]  Size: 6
(a) [ 9.. 9] [ 9..11] [ 9..11]  Size: 9     no change
(b) [10..11] [ 9.. 9] [ 9..11]  Size: 6     no change
(c) [10..11] [10..11] [ 9.. 9]  Size: 4     no change

must now cmp all of the above with box (4)  no change
(4) [11..12] [11..12] [13..13]  Size: 4
(a) [ 9.. 9] [ 9..11] [ 9..11]  Size: 9     no change
(b) [10..11] [ 9.. 9] [ 9..11]  Size: 6     no change
(c) [10..11] [10..11] [ 9.. 9]  Size: 4     no change

==============================================================================
After comparing 2nd box to 3rd box

(1) [10..12] [10..12] [10..12]  Size: 27
(2) [13..13] [11..13] [11..13]  Size: 9
(3) [11..12] [13..13] [11..13]  Size: 6
(4) [11..12] [11..12] [13..13]  Size: 4
(5) [ 9.. 9] [ 9..11] [ 9..11]  Size: 9
(6) [10..11] [ 9.. 9] [ 9..11]  Size: 6
(7) [10..11] [10..11] [ 9.. 9]  Size: 4

TOTAL = 65

