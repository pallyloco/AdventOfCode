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
    $self->{-min_fcost} = 0;
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
    delete $todo->{$done};    #### is this right?
    return $self;
}

# ============================================================================
# already_visisted
# ============================================================================
sub _already_visisted {
    my $self = shift;
    my $node = shift;

    #    print "Checking if visisted : <", $node->id, ">\n";
    if ( $self->_visited->{ $node->id } ) {

        #        print "IT WAS VISITED\n";
    }
    else {

        #        print "IT WAS NOT VISITED\n";

        #      print "Already visisted\n";
        #      print "<", join( ">\n<", sort keys %{ $self->_visited } ), ">\n";
        #      my $x = <>;
    }

    return if $self->_visited->{ $node->id };
}

# ============================================================================
# find_until
# ============================================================================
sub find_until {
    my $self          = shift;
    my $final_obj_key = shift;
    my $num;

    while ( my $current = $self->_find_lowest_cost_node() ) {

        # update the user?
        $num++;

        if ( $self->progress_freq && $num % $self->progress_freq == 0 ) {
            $self->progress_sub->($current);
            print "Total to dos ",scalar(keys %{$self->_to_be_visited}),"\n";

            #my $a = <>;

        }

        # we are done?
        last if $current->obj->key == $final_obj_key;

        # current node is visited, so remove from to_be_visited
        $self->_move_node_to_visited($current);

        # get all new neighbours for this node
        foreach my $child_obj ( @{ $current->obj->children } ) {

            #print $child_obj;next;

            my $child_node =
              Node->new( $child_obj, $current->gcost + $child_obj->cost,
                         $current );

            next if $self->_already_visisted($child_node);

            #system ('clear');
            #print "updating node with ", $child_node->id, "\n";
            $self->_update_node( $current, $child_node );

        }

        #die;

    }
    die;
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
sub _already_in_to_be_visited {
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
    my $self     = shift;
    my $current  = shift;
    my $new_node = shift;

    # node already exists, and we can get there more cheaply
    my $existing_node = $self->_already_in_to_be_visited($new_node);
    if ( $existing_node && $new_node->gcost < $existing_node->gcost ) {
        $existing_node->gcost( $new_node->gcost );
        $self->_update_cost_array($existing_node);
    }

    # node does not exist, so create it
    else {
        $new_node->hcost( $new_node->obj->eta );
        $self->_update_cost_array($new_node);
        my $todo = $self->_to_be_visited;
        $todo->{ $new_node->id } = $new_node;
    }
}

# ============================================================================
# update cost array
# ============================================================================
sub _update_cost_array {
    my $self  = shift;
    my $node  = shift;
    my $costs = $self->_by_cost;

    my $fcost = $node->gcost + $node->hcost;
    $self->{-min_fcost} = $fcost if $fcost < $self->{-min_fcost};

    #print "\n\nMY COSTS ARRAY\n";
    push @{ $costs->{$node->gcost} }, $node;

    #print "new node : ",$node->id,"\n";
    foreach my $c ( sort keys %$costs ) {

        #   print "\nFCOST: $c\n";
        foreach my $n ( @{ $costs->{$c} } ) {

            #      print $n->id;
        }
    }

    #my $a=<>;

# need to keep the cost array sorted by closets distance to home
#   @nodes_with_equal_fcost = sort {$a->hcost <=> $b->hcost} @nodes_with_equal_fcost;

    #    $costs->{ $fcost } = \@nodes_with_equal_fcost;

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

    # ------------------------------------------------------------------------
    # find the lowest fcost
    # ------------------------------------------------------------------------

    #  print "Looking for next node\n";
    while (1) {
        my $min_cost = $self->{-min_fcost} || 0;

        #     print "current min_cost is $min_cost\n";

        if ( exists $by_costs->{$min_cost}
             && scalar( @{ $by_costs->{$min_cost} } ) )
        {

            #        print "we have nodes that match\n";
            my $node = shift @{ $by_costs->{$min_cost} };
            next unless $self->_to_be_visited->{ $node->id };

            #        print "this node was not already visited, so good to go\n";
            return $node;

        }
        elsif ( exists $by_costs->{$min_cost} ) {

            #        print "the cost <$min_cost> has no nodes, deleting it\n";
            delete $by_costs->{$min_cost};
        }
        elsif ( scalar( keys %$by_costs ) ) {

            #       print "finding the next min_cost\n";
            $min_cost = undef;
            foreach my $cost ( keys %$by_costs ) {
                $min_cost = $cost unless defined $min_cost;
                $min_cost = $cost < $min_cost ? $cost : $min_cost;
            }

            #       print "new min cost is $min_cost\n";
            $self->{-min_fcost} = $min_cost;
        }
        else {

            #       print "no more nodes\n";
            last;
        }
    }

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
    $self->gcost( shift || 0 );
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

sub gcost {
    my $self = shift;
    $self->{-gcost} = shift if @_;
    return $self->{-gcost};
}

sub hcost {
    my $self = shift;
    $self->{-hcost} = shift if @_;
    if ( not defined $self->{-hcost} ) {
        $self->{-hcost} = $self->obj->eta;
    }
    return $self->{-hcost};
}

sub prev {
    my $self = shift;
    $self->{-prev} = shift if @_;
    return $self->{-prev};
}

1;
