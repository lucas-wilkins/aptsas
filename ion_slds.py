import periodictable

def molecular_sld(elemental_breakdown: list[tuple[str, int]]):

    # TODO: Verify this is correct
    sld = 0.0
    for element, amount in elemental_breakdown:
        atom_sld, cross_section, penetration_depth = periodictable.neutron_scattering(element, wavelength=6.0)
        sld += atom_sld[0]

    return sld / sum([amount for _, amount in elemental_breakdown])

print(molecular_sld([("C", 1)]))
print(molecular_sld([("O", 1)]))
print(molecular_sld([("C", 1), ("O", 2)]))
