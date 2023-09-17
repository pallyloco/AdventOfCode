#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
my $starttime = scalar(localtime),"\n";

open my $fh, "input_day22.txt" or die;

# start with a cuboid of size zero
my @boxes = ();

# ---------------------------------------------------------------------------
# Read in data
# ---------------------------------------------------------------------------
my $line_number = 0;
while ( my $line = <$fh> ) {
    $line_number++;
    chomp $line;
    
    last if $line =~ /^\s*$/;
    my ( $action, $xrange, $yrange, $zrange ) =
      ( $line =~ /^(\w+)\s+x=(.*?),y=(.*?),z=(.*?)$/ );

    # create a new cuboid
    my @coords;
    push @coords, max_min($xrange), max_min($yrange), max_min($zrange);
    my $new_box = Cuboid->new( \@coords );

    # add boxes
    if ( $action eq 'on' ) {
        print "$starttime: ",scalar(localtime),": $line_number ADD $line\n";
        push @boxes, $new_box unless @boxes;
        push @boxes, add_new_box( \@boxes, $new_box );
    }

    # subtract boxes
    if ( $action eq 'off' ) {
        print "$starttime: ",scalar(localtime),": $line_number DELETE $line\n";
        delete_data_box( \@boxes, $new_box ) if @boxes;
    }

#    print "\n\n\nNEW BOX LIST\n";
#    foreach my $b (@boxes) {
#        print "$b\n";
#    }

}

# --------------------------------------------------------------------------
# get total
# --------------------------------------------------------------------------
my $total = 0;
print "\n\n\n\n";
my $i = 0;
foreach my $box (@boxes) {
    $i++;
    print "$i -> $box\n";
    $total = $total + $box->size;
}
print "FINAL ANSWER: $total\n";
print scalar(localtime),"\n";


# ==========================================================================
# delete_data_box
# ==========================================================================
sub delete_data_box {
    my $boxes         = shift;
    my $to_delete_box = shift;
    my $result;

    # foreach box that is already there
    # delete stuff if necessary

    my $ibox = 1;
    foreach my $box (@$boxes) {

#        print "\n------------------\n";
#        print "From   $box\ndelete $to_delete_box\n\n";
        my $leftover = $box->subtract($to_delete_box);
        push @$result, @$leftover;
        
#        foreach my $f (@$result) {
#            print "$ibox => $f\n";
#        }
#        $ibox++;
    }

    # replace data in $boxes with new stuff
    undef @$boxes;
    @$boxes = @$result;
}

# ==========================================================================
# add a new box to the list
# ==========================================================================
sub add_new_box {
    my $boxes   = shift;
    my $new_box = shift;

    # foreach box that is already there (none overlap each other)
    # compare to the new box
    my $to_add = [$new_box];

    foreach my $box (@$boxes) {

        # cmp the new box with one of the original boxes
        # returns possibly more than one box
        my $to_add_later = [];
        foreach my $new_box (@$to_add) {
#            print "\n------------------\n";
#            print "Comparing $box\nwith      $new_box\n\n";

            my $t = $box->intersect($new_box);

            # keep track of all the cut-off pieces
            push @$to_add_later, @$t;
        }

        # add cut off pieces to the array in preparation for comparing
        # with one of the other non-overlapping boxes
#        print "\nResults\n";
#        foreach my $t (@$to_add_later) {
#            print "$t\n";
#        }
        $to_add = $to_add_later;
    }

    # at this point, newer boxes should not intersect with any previous
    # box.
    return @$to_add;

}

# ==========================================================================
# get numbers of the range
# ==========================================================================
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
# subtract
# --------------------------------------------------------------------------
sub subtract {
    my $self         = shift;
    my $delete       = shift;         # cuboids
    my $good         = shift || [];

    # loop until no more cuts, etc to make
    while ($self) {

        # it doesn't intersect at all, keep it
        if ( $self->does_not_intersect($delete) ) {
            push @$good, $self;
         #   print "keeping $self\n";
            last;
        }

        # if it is consumed by $delete totally, $self is no longer good
        last if $delete->does_contain($self);

        # slicing and dicing, check all 6 faces
        my $changed = 0;
        foreach my $axis (qw( x y z)) {
            if ( not $changed ) {
                foreach my $side (qw (max min)) {
                    my $get_side = $axis . $side;
                    my @new = $self->get_sliced_by( $axis, $side, $delete->$get_side );
                    if ( scalar(@new) ) {
                        push @$good, $new[0];
           #             print "Keeping $new[0]\n";
                        $self   = $new[1];
                        $changed = 1;
                        last;
                    }
                }
            }
        }
        last if not $changed;
    }
    # "Subtact: Returning: \n";
    #foreach my $g (@$good) {print "$g\n";}
    
    return $good;
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

    # loop until no more cuts, etc to make
    while ($other) {

        # it doesn't intersect at all, keep it
        if ( $self->does_not_intersect($other) ) {
            # "no intersection $other\n";
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
                    my @new = $other->get_sliced_by( $axis, $side, $self->$get_side );
                    if ( scalar(@new) ) {
                        push @$good, $new[0];
                        # "Keeping $new[0]\n";
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
# get_sliced_by
# --------------------------------------------------------------------------
sub get_sliced_by {
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
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507

answer for above should be:
2758514936282235


MANUAL COMPARISON
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
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



** DELETE

------------------
From   [10..12] [10..12] [10..12]  Size: 27
delete [9..11] [9..11] [9..11]  Size: 27

       [ 9..11] [ 9..11] [ 9..11]  Size: 27
       [10..12] [10..12] [10..12]  Size: 27
  rem  [10..11] [10..12] [10..12]           keep [12..12] [10..12] [10..12]
  rem  [10..11] [10..11] [10..12]           keep [10..11] [12..12] [10..12]
       [10..11] [10..11] [10..11]           keep [10..11] [10..11] [12..12]


Keeping [12..12] [10..12] [10..12]  Size: 9
Keeping [10..11] [12..12] [10..12]  Size: 6
Keeping [10..11] [10..11] [12..12]  Size: 4

------------------
From   [13..13] [11..13] [11..13]  Size: 9
delete [9..11] [9..11] [9..11]  Size: 27


------------------
From   [11..12] [13..13] [11..13]  Size: 6
delete [9..11] [9..11] [9..11]  Size: 27


------------------
From   [11..12] [11..12] [13..13]  Size: 4
delete [9..11] [9..11] [9..11]  Size: 27



