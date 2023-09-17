#!/usr/bin/perl
use strict;
use warnings;

package Layout;


use overload '""' => 'stringify', "==" => 'equals';





my %costs = (
              'A1' => 1,
              'A2' => 1,
              'B1' => 10,
              'B2' => 10,
              'C1' => 100,
              'C2' => 100,
              'D1' => 1000,
              'D2' => 1000,
);
my %creature_types = (
                       'A1' => 0,
                       'A2' => 0,
                       'B1' => 1,
                       'B2' => 1,
                       'C1' => 2,
                       'C2' => 2,
                       'D1' => 3,
                       'D2' => 3
);
my %valid_hallways = (
                       'A1' => 2,
                       'A2' => 2,
                       'B1' => 4,
                       'B2' => 4,
                       'C1' => 6,
                       'C2' => 6,
                       'D1' => 8,
                       'D2' => 8,
);

#########################################################################################
# ----------------------
#  0  1  2  3  4  5  6  7  8  9  10
#        2     4     6     8
#        2     4     6     8
# ----------------------
my $done_str = <<DONE_STR;
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
DONE_STR
my @done_str = split "\n", $done_str;
    my $done_layout = Layout->new();
    $done_layout->set_position( \@done_str );

sub key {
    my $self = shift;
    return "$self";
}
sub final_goal {
    my $self = shift;
    return $done_layout;
}

sub _is_doorway {
    my $self = shift;
    my $spot = shift || die;
    return
         Spot->new( 0, 2 ) == $spot
      || Spot->new( 0, 4 ) == $spot
      || Spot->new( 0, 6 ) == $spot
      || Spot->new( 0, 8 ) == $spot;
}
my @creatures = ( 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2' );

sub _is_valid_spot {
    my $self = shift;
    my $spot = shift;
    return 1 if $spot->row == 0 && $spot->col >= 0 && $spot->col <= 10;
    return ( $spot->row == 1 || $spot->row == 2 )
      && (    $spot->col == 2
           || $spot->col == 4
           || $spot->col == 6
           || $spot->col == 8 );
}

sub _valid_hallway {
    my $self     = shift;
    my $creature = shift;
    my $spot     = shift || die( join ", ", "_valid_hallway", caller() );
    return $spot->row > 0 && $spot->col == $valid_hallways{$creature};
}

sub _valid_doorway {
    my $self     = shift;
    my $creature = shift;
    my $spot     = shift;
    return $spot->row == 0 && $spot->col == 2 * $creature_types{$creature} + 2;
}

sub _hallway_clear {
    my $self    = shift;
    my $hallway = shift;
    return 0 if $self->occupied_by( Spot->new( 1, $hallway ) );

    my $someone = $self->occupied_by( Spot->new( 2, $hallway ) );
    if ($someone) {
        return 1 if $self->_valid_hallway( $someone, Spot->new( 2, $hallway ) );
        return 0;
    }
    return 1;
}

sub _get_all_children {
    my $self = shift;
    my $loc  = $self->locs;
    my %new_children;

    ##### GONNA HARD CODE THE RULES ####

    foreach my $creature ( sort keys %$loc ) {

        # where is the creature currently?
        my $spot = $loc->{$creature};

        # don't move if you are at the bottom of the correct corridor
        next if $spot->row == 2 && $self->_valid_hallway( $creature, $spot );

        # don't move if you are at in the correct hallway, and the guy
        # below you is also in the correct place
        next
          if $spot->row == 1
              && $self->_valid_hallway( $creature, $spot )
              && $self->occupied_by( $spot->down )
              && $self->_valid_hallway( $self->occupied_by( $spot->down ),
                                        $spot );

        # if you can move to your hallway unimpeded, do so.
        my $hallway = $valid_hallways{$creature};
        if ( $spot->col != $hallway ) {
            my $new_spot = $spot;
            my $clear    = 1;
            my $moves    = 0;

            while ( $new_spot->row > 0 ) {
                if ( $self->occupied_by( $new_spot->up ) ) {
                    $clear = 0;
                    last;
                }
                $new_spot = $new_spot->up;
                $moves++;
            }

            if ($clear) {

                my $dir = 'right';
                $dir = 'left' if $new_spot->col > $hallway;
                while ( $new_spot->col != $hallway ) {
                    if ( $self->occupied_by( $new_spot->$dir ) ) {
                        $clear = 0;
                        last;
                    }
                    $new_spot = $new_spot->$dir;
                    $moves++;
                }
            }
            if ($clear) {
                if ( $self->_hallway_clear( $new_spot->col ) ) {
                    $moves++;
                    $new_spot = $new_spot->down;
                    if ( not $self->occupied_by( $new_spot->down ) ) {
                        $new_spot = $new_spot->down;
                        $moves++;
                    }
                    my $copy = $self->copy_locations;
                    $copy->{$creature} = $new_spot;
                    my $cost = $self->cost_of_move( $creature, $moves );
                    $self->add_child( $self->child( $copy, $cost ) );
                    next;
                }
            }
        }

        # more generic moving
        foreach my $mv ( 'up', 'right', 'left' ) {
            next
              if !$self->_is_valid_spot( $spot->$mv )
                  || $self->occupied_by( $spot->$mv );

            # up
            # ... note can only go up left and up right,
            # otherwise you'd be in a doorway
            if ( $mv eq 'up' ) {
                foreach my $leftright ( 'left', 'right' ) {
                    my $upupmv = $spot->up->up->$leftright;
                    my $upmv   = $spot->up->$leftright;
                    my $upup   = $spot->up->up;
                    if ( $self->_is_valid_spot($upupmv) ) {
                        if (    !$self->occupied_by( $spot->up )
                             && !$self->occupied_by($upup)
                             && !$self->occupied_by($upupmv) )
                        {
                            my $copy = $self->copy_locations;
                            $copy->{$creature} = $upupmv;
                            my $cost = $self->cost_of_move( $creature, 3 );
                            my $child = $self->child( $copy, $cost );
                            $self->add_child($child);
                        }
                    }
                    else {
                        if (    !$self->occupied_by( $spot->up )
                             && !$self->occupied_by($upmv) )
                        {
                            my $copy = $self->copy_locations;
                            $copy->{$creature} = $upmv;
                            my $cost = $self->cost_of_move( $creature, 2 );
                            my $child = $self->child( $copy, $cost );
                            $self->add_child($child);
                        }

                    }
                }
                next;
            }

            # right or left, go into hallway if you can
            my $new_spot = $spot->$mv;

            # if you are in a valid doorway,
            if ( $self->_valid_doorway( $creature, $new_spot ) ) {

                # move into it if it is clear, else continue on
                if ( $self->_hallway_clear( $new_spot->col ) ) {
                    my $copy = $self->copy_locations;
                    $copy->{$creature} = $new_spot->down;
                    my $cost = $self->cost_of_move( $creature, 2 );
                    $self->add_child( $self->child( $copy, $cost ) );
                }

                if ( !$self->occupied_by( $new_spot->$mv ) ) {
                    my $copy = $self->copy_locations;
                    $copy->{$creature} = $new_spot->$mv;
                    my $cost = $self->cost_of_move( $creature, 2 );
                    $self->add_child( $self->child( $copy, $cost ) );
                }
            }
            elsif ( $self->_is_doorway($new_spot) ) {
                if ( !$self->occupied_by( $new_spot->$mv ) ) {
                    my $copy = $self->copy_locations;
                    $copy->{$creature} = $new_spot->$mv;
                    my $cost = $self->cost_of_move( $creature, 2 );
                    $self->add_child( $self->child( $copy, $cost ) );
                }
            }
            else {
                my $copy = $self->copy_locations;
                $copy->{$creature} = $new_spot;
                my $cost = $self->cost_of_move( $creature, 1 );
                $self->add_child( $self->child( $copy, $cost ) );
            }

        }
    }
}

sub new { return bless { -locs => {} } }
sub locs { my $self = shift; return $self->{-locs}; }

sub children {
    my $self = shift;
    if ( !defined $self->{-children} ) {
        $self->{-children} = [];
        $self->_get_all_children;
    }
    return $self->{-children};
}

sub add_child {
    my $self = shift;
    my $new = shift || die( join ", ", "add_child", caller() );

    #print "NEW CHILD: $new\n";
    my $children = $self->{-children};
    push @$children, $new;
    return $self;
}

sub child {
    my $self    = shift;
    my $new_loc = shift;
    my $cost    = shift;
    my $child   = Layout->new();
    $child->parent($self);
    $child->{-locs} = $new_loc;
    $child->cost($cost);
    return $child;
}

sub parent {
    my $self = shift;
    $self->{-parent} = shift if @_;
    return $self->{-parent};
}

sub cost {
    my $self = shift;
    $self->{-cost} = shift if @_;
    return $self->{-cost} || 0;
}

sub copy_locations {
    my $self = shift;
    my $loc  = $self->locs;
    my %copy;
    foreach my $key ( keys %$loc ) {
        $copy{$key} = $loc->{$key};
    }
    return \%copy;

}

sub set_position {
    my $self  = shift;
    my $locs  = $self->locs;
    my $lines = shift;
    my %used;

    # throw away 1st line
    shift @$lines;

    # foreach row
    foreach my $row ( 0 .. 2 ) {
        my $col = 0;
        foreach my $c ( $lines->[$row] =~ /([.A-D])/g ) {
            $used{$c}++;

            if ( $row == 0 ) {
                $locs->{ $c . $used{$c} } = Spot->new( $row, $col )
                  if $c =~ /[A-D]/;
                $col++;
            }
            else {
                if ( $col < 2 ) { $col = 2; }
                else            { $col += 2; }
                $locs->{ $c . $used{$c} } = Spot->new( $row, $col )
                  if $c =~ /[A-D]/;
            }
        }
    }
}

sub cost_of_move {
    my $self        = shift;
    my $creature    = shift;
    my $num_squares = shift;
    return $costs{$creature} * $num_squares;
}

sub occupied_by {
    my $self = shift;
    my $spot = shift;
    die("\n") unless ref $spot;
    my $locs = $self->{-locs};
    foreach my $creature ( keys %$locs ) {
        return $creature
          if $locs->{$creature} == $spot;
    }
    return;

}

sub stringify {
    my $self = shift;
    return $self->{-string} if defined $self->{-string};
    my $locs = $self->locs;
    my $str  = "\n";
    foreach my $row ( 0 .. 2 ) {
        foreach my $col ( 0 .. 10 ) {
            my $place_holder = " ";
            $place_holder = "."
              if $self->_is_valid_spot( Spot->new( $row, $col ) );
            my $whos_there = $self->occupied_by( Spot->new( $row, $col ) );
            $whos_there = $whos_there || $place_holder;
            $whos_there = substr( $whos_there, 0, 1 );
            $str .= "$whos_there ";
        }
        $str .= "\n";
    }
    $self->{-string} = $str;
    return $str;
}

sub equals {
    my $self  = shift;
    my $other = shift;
    return "$self" eq "$other";
}

package Spot;
use overload "==" => "equals", '""' => "stringification";

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



1;