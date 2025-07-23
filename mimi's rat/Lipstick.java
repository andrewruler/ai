public enum Lipstick {


    CHANEL("France", 61, "90 Jour"),
    DIOR("France", 61, "77 Candy"),
    YSL("France", 57, "44B Nude Lavalliere"),
    TOM_FORD("USA", 78, "38 Nude Coast"),
    ARMANI("Italy", 61, "400 Armani Red"),
    GIVENCHY("France", 57, "333 Le Rouge"),
    GUCCI("Italy", 66, "208 They Met In Argentina"),
    HERMES("France", 95, "26 Rose Himalaya"),
    LANCOME("France", 43, "31 Popping Poppy"),
    MAC("Canada", 31, "703 Runway Hit");


    private final String originCountry;
    private final int approxPriceCAD; // ✅ renamed from USD to match usage
    private final String lipstickShade;


    // ✅ Constructor updated
    Lipstick(String originCountry, int approxPriceCAD, String lipstickShade) {
        this.originCountry = originCountry;
        this.approxPriceCAD = approxPriceCAD;
        this.lipstickShade = lipstickShade;
    }


    public String getOriginCountry() {
        return originCountry;
    }


    public int getApproxPriceCAD() {
        return approxPriceCAD;
    }


    public String getLipstickShade() {
        return lipstickShade;
    }


    public String getBrandProfile() {
        return name().replace("_", " ") + " is from " + getOriginCountry() +
       ", it has the shade \"" + getLipstickShade() + "\" priced around $" + getApproxPriceCAD() + " CAD.";
    }
}


