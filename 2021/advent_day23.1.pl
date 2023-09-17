#!/usr/bin/perl
use strict;
use warnings;
use advent_day23_1_library;
use dijkstra;

open my $fh, "input_day23.txt" or die;

my @lines = <$fh>;

my $g = Layout->new();
$g->set_position( \@lines );
my $dijkstra = Dijkstra->new($g);

$dijkstra->progress_sub(
    sub {
        my $node = shift;
        system('clear');
        print $node->id, $node->cost, "\n";
    }
);
$dijkstra->progress_freq(100);

my $start =  scalar(localtime);
my $final_node = $dijkstra->find_until( Layout->final_goal );


system('clear');
print "FINAL ANSWER\n";
print $final_node->id;
print $final_node->cost, "\n";
print "$start\n";
print scalar(localtime),"\n";

# all done
print "\n\nDo you want the path? ";
my $ans = <>;
if ( lc( substr( $ans, 0, 1 ) ) eq 'y' ) {
    my $path = $dijkstra->get_path($final_node) ; 
    foreach my $node (@$path){
        print $node->id, "\n";
      };
}


__DATA__
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
