#!/usr/bin/perl
use strict;
use warnings;
use Math::Trig;

my %scanner;
my @data;
my $converter;
my $scanner = 0;

open my $fh, "input_day19.txt" or die;

while ( my $line = <$fh> ) {
    chomp $line;
    if ( $line =~ /scanner\s+(\d+)/ ) {
        $scanner = $1;
        next;
    }
    if ( $line =~ /^\s*$/ ) {
        process_map( $scanner, \@data );
        undef @data;
        next;
    }
    push @data, [ split ",", $line ];
}
process_map( $scanner, \@data );

my $final_map;

foreach my $b ( keys $scanner{0} ) {
    my $beacon = $scanner{0}{$b};
    $final_map->{ $beacon->{-x} }{ $beacon->{-y} }{ $beacon->{-z} }++;
}

while ( scalar( keys %scanner ) > 1 ) {
    foreach my $other_scanner ( sort keys %scanner ) {
        next if $other_scanner == 0;
        print "\n\n=============\n";
        print "Processing scanner $other_scanner\n";
        my @matches;
        my $number = 0;
        foreach my $b ( keys $scanner{0} ) {
            my $beacon = $scanner{0}{$b};
            foreach my $o ( keys $scanner{$other_scanner} ) {
                my $other = $scanner{$other_scanner}{$o};
                my $cmp   = 0;
                $cmp = ( abs( $beacon->{-min1} - $other->{-min1} ) < .01 );
                $cmp =
                  $cmp && ( abs( $beacon->{-min2} - $other->{-min2} ) < .01 );
                if ($cmp) {
                    push @matches, [ $beacon, $other ];
                }
            }
        }
        my $valid = convert( $scanner{0}, $scanner{$other_scanner}, \@matches );
        if ($valid) {
            delete $scanner{$other_scanner};
        }

    }
}

my $total = 0;
foreach my $i ( keys %$final_map ) {
    foreach my $j ( keys %{ $final_map->{$i} } ) {
        foreach my $k ( keys %{ $final_map->{$i}{$j} } ) {
            $total++;
        }
    }
}

print "\n\nFINAL ANSWER: $total\n";

sub convert {
    my $base_scanner  = shift;
    my $other_scanner = shift;
    my $matches       = shift;
    if (@$matches) {
        my $beacon = $matches->[0][0];
        my $other  = $matches->[0][1];
        find_converter( $beacon, $other );
        my $x1 = $beacon->{-x};
        my $y1 = $beacon->{-y};
        my $z1 = $beacon->{-z};
        my $x2 = $other->{-x};
        my $y2 = $other->{-y};
        my $z2 = $other->{-z};

        ( $x2, $y2, $z2 ) = $converter->( $x2, $y2, $z2 );
        my $dx = $x2 - $x1;
        my $dy = $y2 - $y1;
        my $dz = $z2 - $z1;

        foreach my $match (@$matches) {
            my $beacon = $match->[0];
            my $other  = $match->[1];
            my $x1     = $beacon->{-x};
            my $y1     = $beacon->{-y};
            my $z1     = $beacon->{-z};
            my $x2     = $other->{-x};
            my $y2     = $other->{-y};
            my $z2     = $other->{-z};
            my $dx1    = $beacon->{-dx1};
            my $dy1    = $beacon->{-dy1};
            my $dz1    = $beacon->{-dz1};
            ( $x2, $y2, $z2 ) = $converter->( $x2, $y2, $z2 );
            print "($x1,$y1,$z1) ";
            print "(", $x2 - $dx, ",", $y2 - $dy, ",", $z2 - $dz, ")\n";
        }

        my $tmp;
        my $number = 0;
        foreach my $o ( keys $other_scanner ) {
            my $other = $other_scanner->{$o};
            my ( $x2, $y2, $z2 ) =
              $converter->( $other->{-x}, $other->{-y}, $other->{-z} );
            $x2 = $x2 - $dx;
            $y2 = $y2 - $dy;
            $z2 = $z2 - $dz;

            $tmp->{$x2}{$y2}{$z2}++;
            $number++ if $final_map->{$x2}{$y2}{$z2};
        }
        if ( $number > 11 ) {
            foreach my $i ( keys %$tmp ) {
                foreach my $j ( keys %{ $tmp->{$i} } ) {
                    foreach my $k ( keys %{ $tmp->{$i}{$j} } ) {
                        $final_map->{$i}{$j}{$k} = $tmp->{$i}{$j}{$k}++;
                    }
                }
            }
            my @data;
            foreach my $i ( keys %$final_map ) {
                foreach my $j ( keys %{ $final_map->{$i} } ) {
                    foreach my $k ( keys %{ $final_map->{$i}{$j} } ) {
                        push @data, [ $i, $j, $k ];
                    }
                }
            }
            process_map( 0, \@data );
        }
        print "Number $number\n";
        return $number > 11;

        #convert($scanner{1},$converter);
    }
}

sub find_converter {
    my $beacon = shift;
    my $other  = shift;

    # find rotation
    # x in positive direction
    if ( ( $beacon->{-dx1} ) == ( $other->{-dx1} ) ) {    # x = x
        if ( ( $beacon->{-dy1} ) == $other->{-dy1} ) {    # y = y
            $converter = sub { return ( $_[0], $_[1], $_[2] ); };    # z = z
        }
        elsif ( -$beacon->{-dy1} == $other->{-dy1} ) {               # y = -y
            $converter = sub { return ( $_[0], -$_[1], -$_[2] ); };    # z = -z
        }
        elsif ( -$beacon->{-dy1} == $other->{-dz1} ) {                 # y = -z
            $converter = sub { return ( $_[0], -$_[2], $_[1] ); };     # z = y
        }
        else {                                                         # y = z
            $converter = sub { return ( $_[0], $_[2], -$_[1] ); };     # z = -y
        }
    }

    if ( ( $beacon->{-dy1} ) == ( $other->{-dx1} ) ) {                 # y = x
        if ( ( $beacon->{-dx1} ) == $other->{-dz1} ) {                 # x = z
            $converter = sub { return ( $_[2], $_[0], $_[1] ); };      # z = y
        }
        elsif ( -$beacon->{-dx1} == $other->{-dy1} ) {                 # x = -y
            $converter = sub { return ( -$_[1], $_[0], $_[2] ); };     # z = z
        }
        elsif ( $beacon->{-dx1} == $other->{-dy1} ) {                  # x = y
            $converter = sub { return ( $_[1], $_[0], -$_[2] ); };     # z = -z
        }
        else {                                                         # x = -z
            $converter = sub { return ( -$_[2], $_[0], -$_[1] ); };    # z = -y
        }

    }
    if ( ( -$beacon->{-dx1} ) == ( $other->{-dx1} ) ) {                # x = -x
        if ( ( -$beacon->{-dy1} ) == $other->{-dy1} ) {                # y = -y
            $converter = sub { return ( -$_[0], -$_[1], $_[2] ); };    # z = z
        }
        elsif ( -$beacon->{-dy1} == $other->{-dz1} ) {                 # y = -z
            $converter = sub { return ( -$_[0], -$_[2], -$_[1] ); };    # z = -y
        }
        elsif ( $beacon->{-dy1} == $other->{-dy1} ) {                   # y = y
            $converter = sub { return ( -$_[0], $_[1], -$_[2] ); };     # z = -z
        }
        else {                                                          # y = z
            $converter = sub { return ( -$_[0], $_[2], $_[1] ); };      # z = y
        }
    }
    if ( ( -$beacon->{-dy1} ) == ( $other->{-dx1} ) ) {                 # y = -x
        if ( ( $beacon->{-dx1} ) == $other->{-dy1} ) {                  # x = y
            $converter = sub { return ( $_[1], -$_[0], $_[2] ); };      # z = z
        }
        elsif ( $beacon->{-dx1} == $other->{-dz1} ) {                   # x = z
            $converter = sub { return ( $_[2], -$_[0], -$_[1] ); };     # z = -y
        }
        elsif ( -$beacon->{-dx1} == $other->{-dy1} ) {                  # x = -y
            $converter = sub { return ( -$_[1], -$_[0], -$_[2] ); };    # z = -z
        }
        else {                                                          # x = -z
            $converter = sub { return ( -$_[2], -$_[0], $_[1] ); };     # z = y
        }
    }
    if ( ( -$beacon->{-dz1} ) == ( $other->{-dx1} ) ) {                 # z = -x
        if ( -( $beacon->{-dy1} ) == $other->{-dy1} ) {                 # y = -y
            $converter = sub { return ( -$_[2], -$_[1], -$_[0] ); };    # x = -z
        }
        elsif ( $beacon->{-dy1} == $other->{-dy1} ) {                   # y = y
            $converter = sub { return ( $_[2], $_[1], -$_[0] ); };      # x = z
        }
        elsif ( -$beacon->{-dy1} == $other->{-dz1} ) {                  # y = -z
            $converter = sub { return ( $_[1], -$_[2], -$_[0] ); };     # x = y
        }
        else {                                                          # y = z
            $converter = sub { return ( -$_[1], $_[2], -$_[0] ); };     # x = -y
        }
    }
    if ( ( $beacon->{-dz1} ) == ( $other->{-dx1} ) ) {                  # z = x
        if ( -( $beacon->{-dy1} ) == $other->{-dy1} ) {                 # y = -y
            $converter = sub { return ( $_[2], -$_[1], $_[0] ); };      # x = z
        }
        elsif ( $beacon->{-dy1} == $other->{-dy1} ) {                   # y = y
            $converter = sub { return ( -$_[2], $_[1], $_[0] ); };      # x = -z
        }
        elsif ( $beacon->{-dy1} == $other->{-dz1} ) {                   # y = z
            $converter = sub { return ( $_[1], $_[2], $_[0] ); };       # x = y
        }
        else {                                                          # y = -z
            $converter = sub { return ( -$_[1], -$_[2], $_[0] ); };     # x = -y
        }
    }

}

sub process_map {
    my $scanner = shift;
    my $data    = shift;

    foreach my $beacon (@$data) {
        my ( $x1, $y1, $z1 ) = @$beacon;

        my ( $minx, $mminx, $miny, $mminy, $minz, $mminz ) =
          ( 100000, 100000, 100000, 100000, 100000, 100000 );

        my ( $min1, $min2 ) = ( 100000, 100000 );
        my $angle = 0;
        my ( $dx1, $dy1, $dz1, $dx2, $dy2, $dz2 ) =
          ( 100000, 100000, 100000, 100000, 100000, 100000 );

        foreach my $other (@$data) {

            # find the two closest neighbours
            my ( $x2, $y2, $z2 ) = @$other;
            next if $x1 == $x2 && $y1 == $y2 && $z1 == $z2;
            my $d =
              sqrt( ( $x2 - $x1 )**2 + ( $y2 - $y1 )**2 + ( $z2 - $z1 )**2 );
            if ( $min1 < $min2 ) {
                if ( $d < $min2 ) {
                    $min2 = $d;
                    $dx2  = $x2 - $x1;
                    $dy2  = $y2 - $y1;
                    $dz2  = $z2 - $z1;
                }
            }
            else {
                if ( $d < $min1 ) {
                    $min1 = $d;
                    $dx1  = $x2 - $x1;
                    $dy1  = $y2 - $y1;
                    $dz1  = $z2 - $z1;
                }
            }

            #print sqrt($x1*$x1 + $y1*$y1 + $z1*$z1),"\n";
            #print sqrt($x2*$x2 + $y2*$y2 + $z2*$z2),"\n";
            #print $x1*$x2 + $y1*$y2 + $z1*$z2,"\n";
            $angle = acos(
                           ( $x1 * $x2 + $y1 * $y2 + $z1 * $z2 ) / (
                                     sqrt( $x1 * $x1 + $y1 * $y1 + $z1 * $z1 ) *
                                       sqrt( $x2 * $x2 + $y2 * $y2 + $z2 * $z2 )
                           )
            );

            #print "$angle\n";
            #die;

        }
        if ( $min1 > $min2 ) {
            my $tmp = $min1;
            $min1 = $min2;
            $min2 = $tmp;
            $tmp  = $dx1;
            $dx1  = $dx2;
            $dx2  = $tmp;
            $tmp  = $dy1;
            $dy1  = $dy2;
            $dy2  = $tmp;
            $tmp  = $dz1;
            $dz1  = $dz2;
            $dz2  = $tmp;

        }

        #  $scanner{$scanner}{"$x1,$y1,$z1"}{-angle}  = $angle;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-min1} = $min1;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-min2} = $min2;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-x}    = $x1;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-y}    = $y1;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-z}    = $z1;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-dx1}  = $dx1;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-dy1}  = $dy1;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-dz1}  = $dz1;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-dx2}  = $dx2;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-dy2}  = $dy2;
        $scanner{$scanner}{"$x1,$y1,$z1"}{-dz2}  = $dz2;

        # $scanner{$scanner}{"$x1,$y1,$z1"}{-minx}  = $minx;
        # $scanner{$scanner}{"$x1,$y1,$z1"}{-mminx} = $mminx;
        # $scanner{$scanner}{"$x1,$y1,$z1"}{-miny}  = $miny;
        # $scanner{$scanner}{"$x1,$y1,$z1"}{-mminy} = $mminy;
        # $scanner{$scanner}{"$x1,$y1,$z1"}{-minz}  = $minz;
        # $scanner{$scanner}{"$x1,$y1,$z1"}{-mminz} = $mminz;
    }
}
__DATA__
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
