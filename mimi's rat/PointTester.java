public class PointTester {
    public static void main(String[] args) {
        Point p1 = new Point(3, 4);
        Point p2 = new Point(6, 8);

        p1.displayCoordinate();
        p2.displayCoordinate();

        System.out.println("Distance: " + p1.distance(p2));
        System.out.println("Difference: (" + p1.difference(p2).getX() + ", " + p1.difference(p2).getY() + ")");
        System.out.println("Midpoint: (" + p1.midpoint(p2).getX() + ", " + p1.midpoint(p2).getY() + ")");
        System.out.println("Sum: (" + p1.sum(p2).getX() + ", " + p1.sum(p2).getY() + ")");
        System.out.println("Slope: " + p1.slope(p2));
        System.out.println("Y-Intercept: " + p1.yIntercept(p2));
        p1.linearEquation(p2);
    }
}
