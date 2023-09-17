#!/usr/bin/perl
use strict;
use warnings;

my @lines = <DATA>;

my $g = Layout->new();
$g->set_position( \@lines );
#print "Cost of moving D 3x  = ",$g->cost_of_move("D1",3),"\n";die;

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

# dijkstra
my %visited_nodes;
my %to_be_visited_nodes;
$to_be_visited_nodes{$g} = Node->new($g);

while ( my $current_node = find_lowest_cost_vertex() ) {

    #    my $a = <>;
    system('clear');
    print $current_node->location;
    print $current_node->cost, "\n";
    last if $current_node->location == $done_layout;

    my $layout = $current_node->location;

    # current node is visited, so remove from to_be_visited
    $visited_nodes{$layout}++;
    delete $to_be_visited_nodes{$layout};

    # get all new neighbours for this node
    my $children = $layout->children;

    foreach my $child (@$children) {

        # if we have already been there, don't go back
        next if exists $visited_nodes{$child};

        # what is the new current costs
        my $cost = $current_node->cost + $child->cost;

        # updated previously tested nodes if appropriate
        if ( exists $to_be_visited_nodes{$child} ) {
            if ( $cost < $to_be_visited_nodes{$child}->cost ) {
                $to_be_visited_nodes{$child}->cost($cost);
                $to_be_visited_nodes{$child}->location($child);
                $to_be_visited_nodes{$child}->prev($current_node);
            }
            next;
        }

        # this is a 'new' neighbour, add it to the list
        $to_be_visited_nodes{$child} =
          Node->new( $child, $cost, $current_node );
    }

}

sub find_lowest_cost_vertex {
    my $min;
    my $lowest;
    foreach my $nodekey ( keys %to_be_visited_nodes ) {
        my $node = $to_be_visited_nodes{$nodekey};
        $lowest = $node       unless defined $min;
        $min    = $node->cost unless defined $min;
        if ( $node->cost < $min ) {
            $lowest = $node;
            $min    = $node->cost;
        }
    }
    return $lowest;
}

#########################################################################################
package Node;

sub new {
    my $class = shift;
    my $self = bless {};
    $self->location( shift || Location->new() );
    $self->cost( shift || 0 );
    $self->prev(shift);
    return $self;
}

sub location {
    my $self = shift;
    $self->{-location} = shift if @_;
    return $self->{-location};
}

sub cost {
    my $self = shift;
    $self->{-cost} = shift if @_;
    return $self->{-cost};
}

sub prev {
    my $self = shift;
    $self->{-prev} = shift if @_;
    return $self->{-prev};
}

#########################################################################################
# ----------------------
#  0  1  2  3  4  5  6  7  8  9  10
#        2     4     6     8
#        2     4     6     8
# ----------------------

package Layout;
use overload '""' => 'stringify', "==" => 'equals';

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
    my $type     = ord( substr( $creature, 0, 1 ) ) - ord('A');
    return $spot->row > 0 && $spot->col == 2 * $type + 2;
}

sub _valid_doorway {
    my $self     = shift;
    my $creature = shift;
    my $spot     = shift;
    my $type     = ord( substr( $creature, 0, 1 ) ) - ord('A');
    return $spot->row == 0 && $spot->col == 2 * $type + 2;
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

        # if you are in the correct hallway and no one is below you, move down
        if (    $spot->row == 1
             && $self->_valid_hallway( $creature, $spot )
             && not $self->occupied_by( $spot->down ) )
        {
            my $copy = $self->copy_locations;
            $copy->{$creature} = $spot->down;
            die unless $self->_is_valid_spot( $spot->down );
            my $cost = $self->cost_of_move( $creature, 1 );
            $self->add_child( $self->child( $copy, $cost ) );
            next;
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
                            die unless $self->_is_valid_spot($upupmv);
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
                            if (!$self->_is_valid_spot( $upmv )) {
                                print $child;
                                print "$mv... OLD $spot, NEW: ",$spot->$upmv,"\n";
                            }
                            die
                              unless $self->_is_valid_spot( $upmv )
                            ;
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
                    die unless $self->_is_valid_spot( $new_spot->down );
                    my $cost = $self->cost_of_move( $creature, 2 );
                    $self->add_child( $self->child( $copy, $cost ) );
                }

                if ( !$self->occupied_by( $new_spot->$mv ) ) {
                    my $copy = $self->copy_locations;
                    $copy->{$creature} = $new_spot->$mv;
                    my $cost = $self->cost_of_move( $creature, 2 );
                    die unless $self->_is_valid_spot( $new_spot->$mv );
                    $self->add_child( $self->child( $copy, $cost ) );
                }
            }
            elsif ( $self->_is_doorway($new_spot) ) {
                if ( !$self->occupied_by( $new_spot->$mv ) ) {
                    my $copy = $self->copy_locations;
                    $copy->{$creature} = $new_spot->$mv;
                    die unless $self->_is_valid_spot( $new_spot->$mv );
                    my $cost = $self->cost_of_move( $creature, 2 );
                    $self->add_child( $self->child( $copy, $cost ) );
                }
            }
            else {
                my $copy = $self->copy_locations;
                $copy->{$creature} = $new_spot;
                die unless $self->_is_valid_spot($new_spot);
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

sub construct_node_key {
    my $self = shift;
    my $locs = $self->locs;
    my $key  = "";
    foreach my $c ( sort keys %$locs ) {
        $key .= $c . $locs->{$c} . ", ";
    }
    return $key;
}

sub cost_of_move {
    my $self         = shift;
    my $creature     = shift;
    my $num_squares  = shift;
    my $creature_num = ord( substr( $creature, 0, 1 ) ) - ord('A');
    return 10**($creature_num) * $num_squares;
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

package main;

__DATA__
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
