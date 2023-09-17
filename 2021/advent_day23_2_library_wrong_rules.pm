#!/usr/bin/perl

package Layout;
use strict;
use warnings;
use overload '""' => '_stringify', "==" => '_equals';

# =============================================================================
# class constants, etc
# =============================================================================
my $MAX_ROW = 4;
my $MAX_COL = 10;
my %COSTS = (
              'A1' => 1,
              'A2' => 1,
              'B1' => 10,
              'B2' => 10,
              'C1' => 100,
              'C2' => 100,
              'D1' => 1000,
              'D2' => 1000,
              'A3' => 1,
              'A4' => 1,
              'B3' => 10,
              'B4' => 10,
              'C3' => 100,
              'C4' => 100,
              'D3' => 1000,
              'D4' => 1000,
);
my %TOKEN_TYPES = (
                    'A1' => 0,
                    'A2' => 0,
                    'B1' => 1,
                    'B2' => 1,
                    'C1' => 2,
                    'C2' => 2,
                    'D1' => 3,
                    'D2' => 3,
                    'A3' => 0,
                    'A4' => 0,
                    'B3' => 1,
                    'B4' => 1,
                    'C3' => 2,
                    'C4' => 2,
                    'D3' => 3,
                    'D4' => 3
);
my %VALID_HALLWAYS = (
                       'A1' => 2,
                       'A2' => 2,
                       'B1' => 4,
                       'B2' => 4,
                       'C1' => 6,
                       'C2' => 6,
                       'D1' => 8,
                       'D2' => 8,
                       'A3' => 2,
                       'A4' => 2,
                       'B3' => 4,
                       'B4' => 4,
                       'C3' => 6,
                       'C4' => 6,
                       'D3' => 8,
                       'D4' => 8,
);

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
  #A#B#C#D#
  #A#B#C#D#
  ######### 
DONE_STR

my @done_str = split "\n", $done_str;
my $DONE_LAYOUT = Layout->new();
$DONE_LAYOUT->set_position( \@done_str );

# =============================================================================
# new
# =============================================================================
sub new { return bless { -token_locations => {} } }

# =============================================================================
# key - uniquely defines a valid layou
# =============================================================================

sub key {
    my $self = shift;
    return "$self";
}

# =============================================================================
# final goal - what is our 'end point'
# =============================================================================
sub final_goal {
    my $self = shift;
    return $DONE_LAYOUT;
}

# =============================================================================
# based on a set of strings, set initial conditions
# =============================================================================
sub set_position {
    my $self  = shift;
    my $lines = shift;
    my %used;

    # throw away 1st line
    shift @$lines;

    # foreach row
    foreach my $row ( 0 .. $MAX_ROW ) {
        my $col = -1;    # skip the first column which is a '#'

        # find all empty spots, and spots with tokens
        foreach my $c ( split "", $lines->[$row] ) {

            # need to keep track of individual tokens, even if they
            # are of the same type
            $used{$c}++;

            # keep track of all the tokens
            $self->_set_token_location( $c . $used{$c},
                                        Spot->new( $row, $col ) )
              if $c =~ /[A-Z]/;

            $col++;
        }
    }
}

# =============================================================================
# return all the new possible locations, starting from here
# =============================================================================
sub children {
    my $self = shift;
    if ( !defined $self->{-children} ) {
        $self->{-children} = [];
        $self->_get_all_children;
    }
    return $self->{-children};
}

# =============================================================================
# what does is cost to move here, from the parent
# =============================================================================
sub cost {
    my $self = shift;
    $self->{-cost} = shift if @_;
    return $self->{-cost} || 0;
}

# =============================================================================
# estimated cost to reaching goal
# =============================================================================
sub eta {
    my $self = shift;
    my $cost = 0;
    foreach my $token ( keys %TOKEN_TYPES ) {
        $cost += $self->_cost_of_move( $token, $self->_eta($token) );
    }
    return $cost;
}

sub _eta {
    my $self  = shift;
    my $token = shift;
    my $spot  = $self->_where_is($token);
    return unless $spot;

    my $hallway = $VALID_HALLWAYS{$token};

    return 0 unless $spot->col != $hallway;
    my $moves = 0;

    # -------------------------------------------------------------------------
    # if we are in the correct hallway, and nobody who doesn't belong there
    # is underneath, then no cost
    # -------------------------------------------------------------------------
    my $ok = 0;
    if ( $self->_valid_hallway( $token, $spot ) ) {
        $ok = 1;
        foreach my $row ( $spot->row + 1 .. $MAX_ROW ) {
            my $someone = $self->_occupied_by( Spot->new( $row, $spot->col ) );
            if ( $someone && $TOKEN_TYPES{$someone} != $TOKEN_TYPES{$token} ) {
                $ok = 0;
                last;
            }
        }
    }

    return 0 if $ok;

    # -------------------------------------------------------------------------
    # going up
    # -------------------------------------------------------------------------
    my @up_moves;
    foreach my $row ( 0 .. $spot->row - 1 ) {
        $moves++;
    }

    # -------------------------------------------------------------------------
    # going horizontal
    # -------------------------------------------------------------------------
    my @horiz_moves;
    my @range = ( $spot->col + 1 .. $hallway );
    @range = ( $hallway .. $spot->col - 1 ) if $spot->col > $hallway;
    foreach my $col (@range) {
        $moves++;
    }

    # -------------------------------------------------------------------------
    # going down
    # -------------------------------------------------------------------------
    foreach my $row ( 1 .. $MAX_ROW ) {

        #       $moves++;
    }
    return $moves;
}

# =============================================================================
# is the spot a doorway?
# =============================================================================
sub _is_doorway {
    my $self = shift;
    my $spot = shift || die;
    if ( ( $spot->row ) == 0 ) {
        return grep { $_ == $spot->col } values %VALID_HALLWAYS;
    }
    return 0;
}

# =============================================================================
# is this a valid spot (part of the game play)
# =============================================================================
sub _is_valid_spot {
    my $self = shift;
    my $spot = shift;
    return 1 if $spot->row == 0 && $spot->col >= 0 && $spot->col <= $MAX_COL;
    return 0 if $spot->row > $MAX_ROW;
    return grep { $_ == $spot->col } values %VALID_HALLWAYS;
}

# =============================================================================
# is this a valid hallway for the specified token
# =============================================================================
sub _valid_hallway {
    my $self  = shift;
    my $token = shift;
    my $spot  = shift || die( join ", ", "_valid_hallway", caller() );
    return $spot->row > 0 && $spot->col == $VALID_HALLWAYS{$token};
}

# =============================================================================
# is this a valid doorway for the specified token
# =============================================================================
sub _valid_doorway {
    my $self  = shift;
    my $token = shift;
    my $spot  = shift;
    return $spot->row > 0 && $spot->col == $VALID_HALLWAYS{$token};
}

# =============================================================================
# is this hallway clear
# 1) completely unoccupied or
# 2) occupied by only valid tokens for this hallway
# NB: tokens always fall to the lowest location
# =============================================================================
sub _hallway_clear {
    my $self    = shift;
    my $hallway = shift;

    my $clear;
    foreach my $row ( 1 .. $MAX_ROW ) {
        my $spot = Spot->new( $row, $hallway );
        my $someone = $self->_occupied_by($spot);
        $clear = ( not $someone )
          || ( $someone && $self->_valid_hallway( $someone, $spot ) );
        return $clear unless $clear;
    }
    return $clear;
}

# =============================================================================
# get all possible layouts that can be accessed from here
# Restriction... a lot of hard-coding has been done to improve speed, so
#                not all possible layouts are returned
# =============================================================================
sub _get_all_children {
    my $self       = shift;
    my $in_hallway = 0;

    # if I can put something in the hallway, then that is the only move
    foreach my $token ( $self->_all_tokens ) {

        # if you can move to your hallway unimpeded, do so.
        my ( $new_spot, $num_moves ) = $self->_move_to_hallway($token);
        if ($new_spot) {
            $self->_add_child( $self->_copy( $token, $new_spot, $num_moves ) );
            $in_hallway = 1;
            last;
        }

    }

    return if $in_hallway;
    foreach my $token ( $self->_all_tokens ) {
  #      print "\nprocessing $token\n";

        # where is the token currently?
        my $spot = $self->_where_is($token);

        # don't move if you are blocked
        next if $spot->row > 0 && $self->_occupied_by( $spot->up );

        # don't move if you are at in the correct hallway, and the guy
        # below you is also in the correct place
        next if $spot->row > 0 && $self->_hallway_clear( $spot->col );

        # more generic moving
        foreach my $mv ( 'up', 'right', 'left' ) {
  #          print "checking direction $mv\n";
            next
              if !$self->_is_valid_spot( $spot->$mv )
                  || $self->_occupied_by( $spot->$mv );

            # up
            # ... note can only go up left and up right,
            # otherwise you'd be in a doorway
            if ( $mv eq 'up' ) {
                my @moves;
                foreach my $row ( 0 .. $spot->row - 1 ) {
                    push @moves, Spot->new( $row, $spot->col );
                }
                push @moves, Spot->new( 0, $spot->col - 1 );
                if ( $self->_all_clear( \@moves ) ) {
                    $self->_copy( $token, $moves[-1], scalar(@moves) );
                }
                $moves[-1] = Spot->new( 0, $spot->col + 1 );

                if ( $self->_all_clear( \@moves ) ) {
                    $self->_copy( $token, $moves[-1], scalar(@moves) )
                      ;
                }
                next;
            }

            # right or left
            my $new_spot = $spot->$mv;

            # if you are in a valid doorway,
            if ( $self->_is_doorway($new_spot) ) {
                if ( !$self->_occupied_by( $new_spot->$mv ) ) {
                    
                                    $self->_copy( $token, $new_spot->$mv, 2 ) ;
                }
                next;
            }
            $self->_add_child( $self->_copy( $token, $new_spot, 1 ) );

        }
    }
}

# =============================================================================
# What are the locations of the tokens
# =============================================================================
sub _token_locations {
    my $self = shift;
    return $self->{-token_locations};
}

sub _set_token_location {
    my $self  = shift;
    my $token = shift;
    my $spot  = shift;
    $self->_token_locations->{$token} = $spot;
    return $self;
}

sub _all_tokens {
    my $self = shift;
    return sort keys %{ $self->_token_locations };
}

sub _where_is {
    my $self  = shift;
    my $token = shift;
    return $self->_token_locations->{$token};
}

# =============================================================================
# move to hallway
# =============================================================================
sub _move_to_hallway {
    my $self  = shift;
    my $token = shift;
    my $spot  = $self->_where_is($token);

    my $hallway = $VALID_HALLWAYS{$token};

    # if I am already in my own hallway, then what am I doing?
    return unless $spot->col != $hallway;

    # if the hallway isn't clear, there's no point in even trying, is there?
    return unless $self->_hallway_clear($hallway);

    my $clear;

    # -------------------------------------------------------------------------
    # going up
    # -------------------------------------------------------------------------
    my @up_moves;
    foreach my $row ( 0 .. $spot->row - 1 ) {
        push @up_moves, Spot->new( $row, $spot->col );
    }
    $clear = $self->_all_clear( \@up_moves );
    return unless $clear;

    # -------------------------------------------------------------------------
    # going horizontal
    # -------------------------------------------------------------------------
    my @horiz_moves;
    my @range = ( $spot->col + 1 .. $hallway );
    @range = ( $hallway .. $spot->col - 1 ) if $spot->col > $hallway;
    foreach my $col (@range) {
        push @horiz_moves, Spot->new( 0, $col );
    }
    $clear = $self->_all_clear( \@horiz_moves );
    return unless $clear;

    # -------------------------------------------------------------------------
    # going down (we know that the hallway is clear)
    # -------------------------------------------------------------------------
    my @hall_moves;
    foreach my $row ( 1 .. $MAX_ROW ) {
        last if $self->_occupied_by( Spot->new( $row, $hallway ) );
        push @hall_moves, Spot->new( $row, $hallway );
    }
    my $final_spot = $hall_moves[-1];
    my $num_moves  = @up_moves + @horiz_moves + @hall_moves;

    return ( $final_spot, $num_moves );
}

# =============================================================================
# add a child
# =============================================================================
sub _add_child {
    my $self = shift;
    my $new = shift || die( join ", ", "add_child", caller() );
#    print "gave birth to: $new";
#    print "Parent: ", join( ", ", caller ), "\n";
#    my $a        = <>;
    my $children = $self->{-children};
    push @$children, $new;
    return $self;
}

# =============================================================================
# create a child
# =============================================================================
sub _child {
    my $self                = shift;
    my $new_token_locations = shift;
    my $cost                = shift;
    my $child               = Layout->new();
    $child->_parent($self);
    $child->{-token_locations} = $new_token_locations;
    $child->cost($cost);
    return $child;
}

# =============================================================================
# create a copy, with a token in a new position
# =============================================================================
sub _copy {
    my $self      = shift;
    my $token     = shift;
    my $spot      = shift;
    my $num_moves = shift;
    my $copy      = $self->_copy_locations;
    $copy->{$token} = $spot;
    my $cost = $self->_cost_of_move( $token, $num_moves );
    my $child = $self->_child( $copy, $cost );
    $self->_add_child($child);
}

# =============================================================================
# parent
# =============================================================================
sub _parent {
    my $self = shift;
    $self->{-parent} = shift if @_;
    return $self->{-parent};
}

# =============================================================================
# create a copy of the current locations
# ... must be a DIFFERENT hash.
# =============================================================================
sub _copy_locations {
    my $self            = shift;
    my $token_locations = $self->_token_locations;
    my %copy;
    foreach my $key ( keys %$token_locations ) {
        $copy{$key} = $token_locations->{$key};
    }
    return \%copy;

}

# =============================================================================
# how much does it cost to move the number of squares
# =============================================================================
sub _cost_of_move {
    my $self        = shift;
    my $token       = shift;
    my $num_squares = shift;
    return 0 unless $num_squares;
    return $COSTS{$token} * $num_squares;
}

# =============================================================================
# this spot is occupied by?
# =============================================================================
sub _occupied_by {
    my $self = shift;
    my $spot = shift;
    die( "occupied by:\n" . join( ",", caller ) . "\n" ) unless ref $spot;
    my $token_locations = $self->{-token_locations};
    foreach my $token ( keys %$token_locations ) {
        return $token
          if $token_locations->{$token} == $spot;
    }
    return;
}

# =============================================================================
# are any of the spots occupied?
# =============================================================================
sub _all_clear {
    my $self  = shift;
    my $spots = shift;
    foreach my $spot (@$spots) {
        return 0 if $self->_occupied_by($spot);
    }
    return 1;
}

# =============================================================================
# overriding the quotes operatings (or toString for C# and java people)
# =============================================================================
sub _stringify {
    my $self = shift;
    return $self->{-string} if defined $self->{-string};
    my $token_locations = $self->_token_locations;
    my $str             = "\n";

    foreach my $row ( 0 .. $MAX_ROW ) {
        foreach my $col ( 0 .. $MAX_COL ) {
            my $place_holder = " ";
            $place_holder = "."
              if $self->_is_valid_spot( Spot->new( $row, $col ) );

            my $whos_there = $self->_occupied_by( Spot->new( $row, $col ) );
            $whos_there = $whos_there || $place_holder;
            $whos_there = substr( $whos_there, 0, 1 );
            $str .= "$whos_there ";
        }
        $str .= "\n";
    }
    $self->{-string} = $str;
    return $str;
}

# =============================================================================
# overriding the equality operator
# =============================================================================
sub _equals {
    my $self  = shift;
    my $other = shift;
    return "$self" eq "$other";
}

###############################################################################
package Spot;
use strict;
use warnings;

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
