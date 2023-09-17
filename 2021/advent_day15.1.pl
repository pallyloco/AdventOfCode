#!/usr/bin/perl
use strict;
use warnings;
# ===============================================================
package COORD;
# ===============================================================
sub new {
    my $class = shift;
    my $row = shift;
    my $col = shift;
    return bless {-row=>$row,-col=>$col};
}
sub row {
    my $self = shift;
    return $self->{-row};
}
sub col {
    my $self = shift;
    return $self->{-col};
}
sub neighbours {
    my $self = shift;
    my $row = $self->row;
    my $col = $self->col;
    my $height = shift;
    my $width = shift;
    my @n;
    push @n, COORD->new($row-1,$col) unless $row-1 < 0;
    push @n, COORD->new($row+1,$col) unless $row+1 > $height;
    push @n, COORD->new($row,$col-1) unless $col-1 < 0;
    push @n, COORD->new($row,$col+1) unless $col+1 > $width;
    return \@n;
}
# ===============================================================
package MAP;
# ===============================================================
sub new {
    my $class=shift;
    my $map = shift;
    return bless {-map=>$map} ;
}
sub value {
    my $self = shift;
    my $coord = shift;
    $self->map->[$coord->row][$coord->col] = shift if @_;
    return $self->map->[$coord->row][$coord->col];
}
sub map {
    my $self = shift;
    return $self->{-map};
}
sub height {
    my $self = shift;
    $self->{-height} = shift if @_;
    return $self->{-height};
}
sub width {
    my $self = shift;
    $self->{-width} = shift if @_;
    return $self->{-width};
}
  
sub print {
    my $self = shift;
    my $spacing = shift || 1;
    my $height = $self->height || 9;
    my $width = $self->width || 9;
    foreach my $row (0..$height) {
        foreach my $col (0..$width) {
            my $coord = COORD->new($row,$col);
            my $value = $self->value($coord);
            $value = "." unless defined $value;
            if (length($value) < $spacing) {
                $value = " "x($spacing - length($value)).$value;
            }
            print $value;
        }
        print "\n";
    }      
}

# ===============================================================
package MAIN;
# ===============================================================
my @weights;
my $costs = MAP->new([]);
open my $fh, "input_day15.txt" or die;

my $height = 0;
my $width = 0;
while (my $line = <DATA>) {
    chomp $line;
    push @weights, [split "",$line];
    $height++;
    $width = length($line)-1;
}
$height--;

my %done;
my %has_value;

my $current_vertex = COORD->new(0,0);
$costs->value($current_vertex,0);
my $weights = MAP->new(\@weights);

while (1) {
    # calculate neighbours
    print "\nVertex = ",$current_vertex->row,",",$current_vertex->col,"\n";
    foreach my $n (@{$current_vertex->neighbours($height,$width)}) {
        my $key = $n->row .",".$n->col;
        next if exists $done{$key};
        my $cost = $weights->value($n) + $costs->value($current_vertex);
        next if $has_value{$key} && $cost > $costs->value($n);
        $costs->value($n,$cost);
        $has_value{$key} = $n;
    }    
    # set new vertex
    undef $has_value{$current_vertex->row .",".$current_vertex->col};
    $done{$current_vertex->row .",".$current_vertex->col} = $current_vertex;
    
    my $low_cost;
    foreach my $coord (values %has_value) {
        next unless $coord;
        if (! defined $low_cost || $low_cost > $costs->value($coord)) {
            $low_cost = $costs->value($coord);
            $current_vertex = $coord;
        }
    }
    
    $costs->print(4);
   if ($current_vertex->row == $height && $current_vertex->col == $width) {
        print "\n\nRESULT: ",$costs->value($current_vertex);
        last;
    }
}


__DATA__
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
