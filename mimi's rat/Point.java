public class Point {

    private double x;
    private double y;

    public Point() {
        this.x = 0;
        this.y = 0;
    }

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public void displayCoordinate() {
        System.out.println("The x-coordinate is: " + x);
        System.out.println("The y-coordinate is: " + y);
    }

    public double distance(Point point) {
        double dx = this.x - point.x;
        double dy = this.y - point.y;
        return Math.sqrt(dx * dx + dy * dy);
    }

    public Point difference(Point point) {
        return new Point(this.x - point.x, this.y - point.y);
    }

    public Point midpoint(Point point) {
        return new Point((this.x + point.x) / 2, (this.y + point.y) / 2);
    }

    public Point sum(Point point) {
        return new Point(this.x + point.x, this.y + point.y);
    }

    public double slope(Point point) {
        return (point.y - this.y) / (point.x - this.x);
    }

    public double yIntercept(Point point) {
        double m = slope(point);
        return this.y - m * this.x;
    }

    public void linearEquation(Point point) {
        double m = slope(point);
        double b = yIntercept(point);
        System.out.println("y = " + m + "x + " + b);
    }
}
