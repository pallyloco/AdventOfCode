#!/usr/bin/perl

###############################################################################
package AStar;
###############################################################################
use strict;
use warnings;

# ============================================================================
# new
# ============================================================================
sub new {
    my $class     = shift;
    my $start_obj = shift;
    my $self      = bless {};
    $self->_visited(       {} );
    $self->_to_be_visited( {} );
    $self->_by_cost(       {} );
    $self->_start_at_node($start_obj);
    $self->{-max_costs} = 0;
    return $self;
}

# ============================================================================
# add_new_node
# ============================================================================
sub _start_at_node {
    my $self = shift;
    my $obj  = shift;
    my $node = Node->new($obj);
    $self->_to_be_visited->{ $obj->key } = $node;
    my $cost = $self->_by_cost;
    $cost->{0} = [$node];
    return $self;
}

# ============================================================================
# move node to visited
# ============================================================================
sub _move_node_to_visited {
    my $self = shift;
    my $node = shift;
    my $done = $self->_visited;
    $done->{ $node->id }++;
    my $todo = $self->_to_be_visited;
    return $self;
}

# ============================================================================
# already_visisted
# ============================================================================
sub _already_visisted {
    my $self = shift;
    my $node = shift;
    my $done = $self->_visited;
    return if exists $done->{ $node->id };
}

# ============================================================================
# find_until
# ============================================================================
sub find_until {
    my $self          = shift;
    my $final_obj_key = shift;
    my $num;

    while ( my $current = $self->_find_lowest_cost_node() ) {
        $self->_current_node($current);
        $self->{-max_costs} = $self->{-max_costs} > $current->cost ? 
        $self->{-max_costs}: $current->cost;

        # update the user?
        $num++;
        if ( $self->progress_freq && $num % $self->progress_freq == 0 ) {
            $self->progress_sub->($current);
            my $by_costs = $self->_by_cost;

            my @costs = sort { $a <=> $b } keys %$by_costs;
            print $costs[0], "\t",$self->{-max_costs},"\n";

            #    my $a = <>;
        }

        # we are done?
        last if $current->obj->key == $final_obj_key;

        # current node is visited, so remove from to_be_visited
        $self->_move_node_to_visited($current);

        # get all new neighbours for this node
        foreach my $child_obj ( @{ $current->obj->children } ) {

            my $child_node =
              Node->new( $child_obj, $current->cost + $child_obj->cost,
                         $current );
            next if $self->_already_visisted($child_node);
            $self->_update_node( $current, $child_node );

        }

    }
    return $self->_current_node;
}

# ============================================================================
# get_path
# ============================================================================
sub get_path {
    print "PATH inputs ", join ",", @_, "\n";
    my $self      = shift;
    my $node      = shift;
    my $max_nodes = shift || 100;
    my $count     = 0;
    my @nodes     = ($node);
    while ( ( my $next_node = $node->prev ) && $count < $max_nodes ) {
        unshift @nodes, $next_node;
        $node = $next_node;
        $count++;
    }
    return \@nodes;
}

# ============================================================================
# already in visisted nodes?
# ============================================================================
sub _get_to_be_visisted_node {
    my $self = shift;
    my $node = shift;
    my $todo = $self->_to_be_visited;
    return $todo->{ $node->id } if exists $todo->{ $node->id };
    return;
}

# ============================================================================
# update node if exists, else create it
# ============================================================================
sub _update_node {
    my $self          = shift;
    my $current       = shift;
    my $new_node      = shift;
    my $existing_node = $self->_get_to_be_visisted_node($new_node);

    if ( ( $existing_node && $new_node->cost < $existing_node->cost )
         || not $existing_node )
    {
        $self->_to_be_visited->{ $new_node->id } = $new_node;
        $self->_update_cost_array($new_node);
    }
}

# ============================================================================
# update cost array
# ============================================================================
sub _update_cost_array {
    my $self  = shift;
    my $node  = shift;
    my $costs = $self->_by_cost;
    my $x     = $node->obj->eta;

    #  print "eta: $x\n";
    #  print $node->obj;
    #  my $a= <>;
    push @{ $costs->{ $node->cost + $node->obj->eta } }, $node;
    return $self;
}

# ============================================================================
# properties
# ============================================================================
sub progress_sub {
    my $self = shift;
    $self->{-progress_sub} = shift if @_;
    return $self->{-progress_sub} || sub { return };
}

sub progress_freq {
    my $self = shift;
    $self->{-progress_freq} = shift if @_;
    return $self->{-progress_freq} || 0;
}

# ============================================================================
# find the node with the lowest cost
# ============================================================================
sub _find_lowest_cost_node {
    my $self     = shift;
    my $by_costs = $self->_by_cost;

    my @costs = sort { $a <=> $b } keys %$by_costs;

    #   print ("@costs\n");
    my $i = 0;
    while (1) {
        unless ( scalar( @{ $by_costs->{ $costs[$i] } } ) ) {
            delete $by_costs->{ $costs[$i] };
            $i++;
            next;
        }
        last if $i > @costs - 1;
        my $node = shift @{ $by_costs->{ $costs[$i] } };
        next unless $self->_to_be_visited->{ $node->id };
        return $node;
    }
    return;
}

# ============================================================================
# properties
# ============================================================================
sub _visited {
    my $self = shift;
    $self->{-visited} = shift if @_;
    return $self->{-visited};
}

sub _to_be_visited {
    my $self = shift;
    $self->{-to_be_visited} = shift if @_;
    return $self->{-to_be_visited};
}

sub _by_cost {
    my $self = shift;
    $self->{-by_cost} = shift if @_;
    return $self->{-by_cost};
}

sub _current_node {
    my $self = shift;
    $self->{-current_node} = shift if @_;
    return $self->{-current_node};
}

#########################################################################################
package Node;

sub new {
    my $class = shift;
    my $self  = bless {};
    my $obj   = shift
      || die( "\ninvalid object in Node->new\n\t, ", join( ", ", caller() ),
              "\n" );
    $self->obj($obj);
    $self->cost( shift || 0 );
    $self->prev(shift);
    $self->id( $obj->key );
    return $self;
}

sub id {
    my $self = shift;
    $self->{-id} = shift if @_;
    return $self->{-id};
}

sub obj {
    my $self = shift;
    $self->{-obj} = shift if @_;
    return $self->{-obj};
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

1;
