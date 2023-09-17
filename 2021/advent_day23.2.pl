#!/usr/bin/perl
use strict;
use warnings;
use advent_day23_2_library;
use Astar;

open my $fh, "input_day23.txt" or die;
my @inserts = (
'  #D#C#B#A#',
'  #D#B#A#C#',
  );
my @lines = <$fh>;
@lines = (@lines[0..2],@inserts,@lines[3..4]);

my $g = Layout->new();
$g->set_position( \@lines );
my $dijkstra = AStar->new($g);

my $start =  scalar(localtime);
$dijkstra->progress_sub(
    sub {
        my $node = shift;
        system('clear');
        print $node->id, join("\t",$node->hcost + $node->gcost, $node->hcost, $node->gcost),"\n";
        print $start,"\n";
        print scalar(localtime),"\n";
    }
    
);
$dijkstra->progress_freq(100);

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
        print "\n\nCOST: ",$node->cost,"\n";
        print $node->id, "\n";
      };
}


__DATA__
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########