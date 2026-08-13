#Stop-cost model for the Tokaido Shinkansen.
#If anyone is actually testing it out, please use jupyter notebook or Google Colab 

LINE_KM = 515.4
V_MAX = 285.0
ACCEL = 2.6
BRAKE = 2.7
T_TO_270 = 180.0

SERVICES = [
    ("Nozomi (fastest, Mar 2025 timetable)", 141, 4, True),
    ("Kodama 836 (our journey, from the ticket)", 234, 15, True),
    ("Hikari (typical pattern, approximate)", 173, 7, False),
]


def hr(text):
    print("\n" + text)
    print("-" * 74)


def main():
    hr("1. THE JOURNEY AS TICKETED")
    dur = 234
    avg = LINE_KM / (dur / 60)
    print("  duration      %d min (%d h %02d min)" % (dur, dur // 60, dur % 60))
    print("  line length   %.1f km" % LINE_KM)
    print("  mean speed    %.1f / (%d/60) = %.1f km/h" % (LINE_KM, dur, avg))
    print("  ... which is  %.0f%% of the line maximum" % (100 * avg / V_MAX))

    hr("2. THEORETICAL FLOOR - non-stop at line speed")
    floor = LINE_KM / V_MAX * 60
    print("  %.1f / %.0f * 60 = %.1f min" % (LINE_KM, V_MAX, floor))
    print("  no scheduled service can beat this and none comes close,")
    print("  because every service stops at least four times.")

    hr("3. MARGINAL COST OF A STOP - fitted on the two exact services")
    fit = [s for s in SERVICES if s[3]]
    (_, t1, n1, _), (_, t2, n2, _) = fit
    slope = (t2 - t1) / (n2 - n1)
    inter = t1 - slope * n1
    print("  Nozomi   %2d stops   %d min" % (n1, t1))
    print("  Kodama   %2d stops   %d min" % (n2, t2))
    print("  slope     = (%d - %d) / (%d - %d) = %.2f min/stop" % (t2, t1, n2, n1, slope))
    print("  intercept = %d - %.4f * %d = %.1f min" % (t1, slope, n1, inter))
    print()
    print("  intercept vs floor: %.1f vs %.1f  (%+.1f%%)"
          % (inter, floor, 100 * (inter - floor) / floor))
    print("  it lands just BELOW the floor, which no real train can do -")
    print("  so the two-point fit slightly over-blames stops, and %.2f" % slope)
    print("  should be read as an upper bound.")

    hr("4. CHECK ON A SERVICE NOT USED IN THE FIT")
    for label, obs, n, used in SERVICES:
        if used:
            continue
        pred = inter + slope * n
        print("  %s" % label)
        print("    predicted %.1f min, reported about %d  (%+.1f)" % (pred, obs, pred - obs))
        print("    Hikari patterns vary between services, so this is a sanity")
        print("    check, not a validation.")

    hr("5. KINEMATIC COST OF A STOP - what physics alone demands")
    v = V_MAX / 3.6
    a = ACCEL / 3.6
    b = BRAKE / 3.6
    print("  v = %.0f km/h = %.2f m/s" % (V_MAX, v))
    print("  a = %.1f km/h/s = %.3f m/s2" % (ACCEL, a))
    print("  b = %.1f km/h/s = %.3f m/s2" % (BRAKE, b))
    print()
    print("  time lost vs sailing past = time taken - time the same distance")
    print("  would have needed at line speed:")
    la = v / (2 * a)
    lb = v / (2 * b)
    print("    accelerating  v/(2a) = %.1f s" % la)
    print("    braking       v/(2b) = %.1f s" % lb)
    lo = (la + lb) / 60
    print("    total         %.1f s = %.2f min" % (la + lb, lo))
    print()
    print("  but that assumes it holds 2.6 all the way to 285, which it can't:")
    print("  published time to 270 is ~%.0f s, not the %.0f s a constant"
          % (T_TO_270, 270 / ACCEL))
    print("  2.6 would give. taking mean speed over the accel phase as 60-70%")
    print("  of final speed:")
    for frac in (0.60, 0.70):
        lost = T_TO_270 * (1 - frac)
        print("    at %.0f%% -> %.0f s lost accelerating, %.2f min/stop"
              % (frac * 100, lost, (lost + lb) / 60))
    hi = (T_TO_270 * 0.4 + lb) / 60
    print()
    print("  so: %.1f to %.1f min. call it 2." % (lo, hi))

    hr("6. WHERE THE TIME ACTUALLY GOES")
    print("  marginal cost of a stop, measured   %.2f min" % slope)
    print("  of which kinematics                 %.2f to %.2f" % (lo, hi))
    print("  left over (dwell + being passed)    %.2f to %.2f" % (slope - hi, slope - lo))
    print()
    print("  over Kodama 836's 15 intermediate stops. only the first line is")
    print("  calculated from first principles; the second is bounded by the")
    print("  kinematic model; the third is whatever is left of the 234 min.")
    print()
    for k, lab in ((lo, "low "), (hi, "high")):
        print("    %s kinematic estimate: run %.1f + brake/accel %.1f + stand %.1f"
              % (lab, floor, 15 * k, 234 - floor - 15 * k))
    s_lo = 234 - floor - 15 * hi
    s_hi = 234 - floor - 15 * lo
    print()
    print("  -> standing %.0f to %.0f min, i.e. %.0f-%.0f%% of the journey."
          % (s_lo, s_hi, 100 * s_lo / 234, 100 * s_hi / 234))

    hr("7. MEAN SPEEDS FOR THE TEXT")
    for label, mins, n, _ in SERVICES:
        s = LINE_KM / (mins / 60)
        print("  %-42s %6.1f km/h  (%.0f%% of max)" % (label, s, 100 * s / V_MAX))
    # the 1958/1960 benchmarks ran on the conventional line, which is longer
    old_km = 556.4
    for label, mins in [("1958 Kodama ltd exp (debut)", 410),
                        ("1960 Kodama ltd exp (revised)", 390)]:
        print("  %-42s %6.1f km/h  (over %.1f km of conventional line)"
              % (label, old_km / (mins / 60), old_km))


if __name__ == "__main__":
    main()
