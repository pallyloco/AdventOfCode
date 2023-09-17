#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

open my $fh, "input_day22.txt" or die;
my %reboot;

my @updated_ranges;
my $last_action = "";

# =============================================================================
# merge the 'ons' and 'offs' into single range definitions
# =============================================================================

while ( my $line = <DATA> ) {
    my ( $action, $xrange, $yrange, $zrange ) =
      ( $line =~ /^(\w+)\s+x=(.*?),y=(.*?),z=(.*?)$/ );

    if ( $last_action eq $action ) {
        add_range( $updated_ranges[-1], [ $action, $xrange, $yrange, $zrange ] );
    }
    else {
        print "[", join( "],\t[", @{ $updated_ranges[-1] } ), "]\n"
          if @updated_ranges;
        push @updated_ranges, [ $action, $xrange, $yrange, $zrange ];
    }
    $last_action = $action;
}

print "[", join( "],\t[", @{ $updated_ranges[-1] } ), "]\n";

# =============================================================================
# now subtract the offs from the ons (ooh boy)
# =============================================================================
my $final_range = [];
foreach my $range (@updated_ranges) {

    print "\nr: [", join( "],\t[", @{$range } ), "]\n";
    # 1st one, nothing to to do
    unless (@$final_range) {
        $final_range = [ $range->[0],$range->[1],$range->[2],$range->[3]];
        print "f: [", join( "],\t[", @{$final_range } ), "]\n";
        next;
    }
    if ( $range->[0] eq 'off' ) {
        subtract_range( $final_range, $range );
    }
    else {
        add_range( $final_range, $range );
    }
    print "f: [", join( "],\t[", @{$final_range } ), "]\n";

}

# =============================================================================
# calculate the final answer
# =============================================================================
print "\n\n\n";
print $final_range->[1],"\n";
print $final_range->[2],"\n";
print $final_range->[3],"\n";
my @x = eval($final_range->[1]);
my @y = eval($final_range->[2]);
my @z = eval($final_range->[3]);
print scalar(@x)," ",scalar(@y)," ",scalar(@z)," ";
print $final_range->[1],"\n";

print "FINAL ANSWER:   ", scalar(@x) * scalar(@y) * scalar(@z), "\n";
print "supposed to be :",2758514936282235,"\n";

# =============================================================================
# subtract a set from an existing one
# =============================================================================
sub subtract_range {
    my $ranges1 = shift;
    my $ranges2 = shift;
    $ranges1->[1] = subtract_single( $ranges1->[1], $ranges2->[1] );
    $ranges1->[2] = subtract_single( $ranges1->[2], $ranges2->[2] );
    $ranges1->[3] = subtract_single( $ranges1->[3], $ranges2->[3] );
}

sub subtract_single {
    my $range1     = shift;
    my $range2     = shift;
    my @subtracted_sets = ( split ",", $range2 );

    foreach my $subtracted_set (@subtracted_sets) {
        my @range_sets = ( split ",", $range1 );
        my ( $start, $end ) = max_min($subtracted_set);

        my @new_sets;
        foreach my $set (@range_sets) {
            next if $set =~ /^\s*$/;
            my ( $set_start, $set_end ) = max_min($set);

            # does the subtracted range engulf the entirety of the old set?
            if (  $start < $set_start && $end > $set_end ) {
                next;
            }

            # does the new range sit entirety within the old set?
            if ( $start > $set_start && $end < $set_end ) {
                push @new_sets, "$set_start..".($start-1) ;
                push @new_sets, ($end+1)."..$set_end";
                next;
            }

            # does the new range sit partially within the old set?
            if ( $start >= $set_start && $start <= $set_end ) {
                push @new_sets, "$set_start..".($start-1) if $set_start <= $start-1;
                push @subtracted_sets, "$set_end..$end" if $set_end <= $end;
                next;
            }
            push @new_sets, $set;
        }

        # sort
        @new_sets = sort {
            my ( $ma, undef ) = max_min($a);
            my ( $mb, undef ) = max_min($b);
            return $ma <=> $mb;
        } @new_sets;

        # now we have to see if we have overlapping sets
        my @improved;
        my $last_one_merged = 0;
        foreach my $set_number ( 0 .. scalar(@new_sets) - 2 ) {
            my ( $s1, $e1 ) = max_min( $new_sets[$set_number] );
            my ( $s2, $e2 ) = max_min( $new_sets[ $set_number + 1 ] );

            # there is an overlap
            if ( $s1 == $s2 || $e1 > $s2 ) {
                my $end = $e1 > $e2 ? $e1 : $e2;
                push @improved, "$s1..$end";
                $last_one_merged = 1 if $set_number == scalar(@new_sets) - 2;
                next;
            }

            push @improved, $new_sets[$set_number];
        }
        push @improved, $new_sets[-1] unless $last_one_merged;

        # create a new range string, with the sets sorted by minimum values
        $range1 =  join( ",", @improved );
    }
    return $range1;
}

# =============================================================================
# add a set to an existing one
# =============================================================================
sub add_range {
    my $ranges1 = shift;
    my $ranges2 = shift;
    $ranges1->[1] = add_single( $ranges1->[1], $ranges2->[1] );
    $ranges1->[2] = add_single( $ranges1->[2], $ranges2->[2] );
    $ranges1->[3] = add_single( $ranges1->[3], $ranges2->[3] );
}

sub add_single {
    my $range1     = shift;
    my $range2     = shift;
    my @added_sets = ( split ",", $range2 );

    foreach my $added_set (@added_sets) {
        my @range_sets = ( split ",", $range1 );
        my ( $start, $end ) = max_min($added_set);

        my @new_sets;
        my $done = 0;
        foreach my $set (@range_sets) {
            next if $set =~ /^\s*$/;
            my ( $set_start, $set_end ) = max_min($set);

            # does the new range engulf the entirety of the old set?
            if ( !$done && $start < $set_start && $end > $set_end ) {
                push @new_sets, "$start..$end";
                $done++;
                next;
            }

            # does the new range sit entirety within the old set?
            if ( !$done && $start > $set_start && $end < $set_end ) {
                push @new_sets, $set;
                $done++;
                next;
            }

            # does the new range sit partially within the old set?
            if ( !$done && ( $start >= $set_start && $start <= $set_end )
                 || ( $end >= $set_start && $end <= $set_end ) )
            {
                my $new_start = $start < $set_start ? $start : $set_start;
                my $new_end   = $end > $set_end     ? $end   : $set_end;
                push @new_sets, "$new_start..$new_end";
                $done++;
                next;
            }
            push @new_sets, $set;
        }

        # if we got this far, then the set still needs to be added
        push @new_sets, $added_set unless $done;

        # sort
        @new_sets = sort {
            my ( $ma, undef ) = max_min($a);
            my ( $mb, undef ) = max_min($b);
            return $ma <=> $mb;
        } @new_sets;

        # now we have to see if we have overlapping sets
        my @improved;
        my $last_one_merged = 0;
        foreach my $set_number ( 0 .. scalar(@new_sets) - 2 ) {
            my ( $s1, $e1 ) = max_min( $new_sets[$set_number] );
            my ( $s2, $e2 ) = max_min( $new_sets[ $set_number + 1 ] );

            # there is an overlap
            if ( $s1 == $s2 || $e1 > $s2 ) {
                my $end = $e1 > $e2 ? $e1 : $e2;
                push @improved, "$s1..$end";
                $last_one_merged = 1 if $set_number == scalar(@new_sets) - 2;
                next;
            }

            push @improved, $new_sets[$set_number];
        }
        push @improved, $new_sets[-1] unless $last_one_merged;

        # create a new range string, with the sets sorted by minimum values
        $range1 =  join( ",", @improved );
    }
    return $range1;
}

sub max_min {
    my $range = shift;
    my ( $start, $end ) = ( $range =~ /(-?\d+)\.\.(-?\d+)/ );
    return ( $start, $end );
}

__DATA__
on x=-2..2,y=-2..2,z=-2..2
on x=-3..3,y=-1..1,z=-1..1
