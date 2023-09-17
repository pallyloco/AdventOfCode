#!/usr/bin/perl
use strict;
use warnings;

open my $fh, "input_day22.txt" or die;
my %reboot;
my %mins = (
             x => { -min => -50, -max => 50 },
             y => { -min => -50, -max => 50 },
             z => { -min => -50, -max => 50 },
);


while ( my $line = <DATA> ) {
    last if $line =~/^\s*$/;
    my ( $action, $xrange, $yrange, $zrange ) =
      ( $line =~ /^(\w+)\s+x=(.*?),y=(.*?),z=(.*?)$/ );

    my $rangex = get_range($xrange,$mins{x});
    my $rangey = get_range($yrange,$mins{y});
    my $rangez = get_range($zrange,$mins{z});

    my $set = $action eq "on" ? 1 : 0;
    my $test = 0;
#    print $xrange,"\t",$yrange,"\t",$zrange,"\n";
#    print scalar(@$rangex),"\t",scalar(@$rangey),"\t",scalar(@$rangez),"\n";
    foreach my $x ( @$rangex ) {
        foreach my $y ( @$rangey ) {
            foreach my $z ( @$rangez ) {

                $reboot{$x}{$y}{$z} = $set;
            }
        }

    }
}

print "FINAL ANSWER: ", count( \%reboot ), "\n";

sub count {
    my $hash3d = shift;
    my ( $minx, $maxx, $miny, $maxy, $minz, $maxz ) = @_;
    my $count = 0;
    foreach my $x ( sort {$a<=>$b} keys %$hash3d ) {

        foreach my $y ( sort {$a<=>$b} keys %{ $hash3d->{$x} } ) {
            foreach my $z ( sort {$a<=>$b} keys %{ $hash3d->{$x}{$y} } ) {
                $count += $hash3d->{$x}{$y}{$z};
            }
        }

    }
    return $count;
}
sub get_range {
    my $range = shift;
    my $limits = shift;
    my ($start,$end) = ($range =~ /(-?\d+)\.\.(-?\d+)/);
    return [] if $end < $limits->{-min};
    return [] if $start > $limits->{-max};
    $start = $start > $limits->{-min} ? $start : $limits->{-min};
    $end = $end < $limits->{-max} ? $end : $limits->{-max};
    my @a = ($start .. $end);
    return \@a;
}
    
    

__DATA__
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
