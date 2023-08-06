"""Created on Sat Mar 18 09:00:12 2023.

@author: YuxiaoLan
"""

from HTMACat.catkit.gen.adsorption import Builder
from HTMACat.catkit.gratoms import *
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors
import math
from HTMACat.Extract_info import *
from HTMACat.model.Substrate import Slab
from HTMACat.catkit.gen.adsorption import AdsorptionSites
from HTMACat.model.Structure import Structure
import networkx.algorithms.isomorphism as iso
from ase import Atoms
from HTMACat.model.Species import init_from_ads, ABS_Species


class Adsorption(Structure):
    def __init__(self, species: list, sites: list, spec_ads_stable=None, substrate=Slab()):
        if spec_ads_stable is None:
            spec_ads_stable = {
                "NH3": [1],
                "NH2": [2],
                "NH": [2, 4],
                "N": [2, 4],
                "O": [2, 4],
                "OH": [2, 4],
                "NO": [2, 4],
                "H2O": [1],
                "H": [2, 4],
            }
        assert isinstance(species, list), "species should be a list of Species class"
        assert isinstance(species[0], ABS_Species), "species should be a list of Species class"
        assert isinstance(sites, list), "sites should be a list"
        assert sites[0] in ['1', '2'], 'Supports only "1" "2" adsorption sites type for ads!'
        self.species = species
        self.sites = sites
        self.spec_ads_stable = spec_ads_stable
        self.substrate = substrate

    def set_species(self, species):
        self.species = species

    def add_species(self, species):
        self.species.append(species)

    def add_sites(self, sites):
        self.sites.append(sites)

    def get_sites(self):
        return self.sites # ' '.join(self.sites)

    def out_file_name(self):
        ads = []
        ads_str = self.species[0].out_file_name()
        substrate_str = self.substrate.out_file_name()
        vasp_file_str: str = "_".join([substrate_str, ads_str])
        return vasp_file_str

    def out_print(self):
        species_str = []
        for i in range(len(self.species)):
            species_str.append(self.species[i].out_print())

        species_str = " and ".join(species_str)
        substrate_str = self.substrate.out_print()
        print_str = f"{species_str} adsorption on {substrate_str}"
        return print_str

    def construct(self):
        if self.get_sites()[0] == '1':
            if len(self.get_sites()) == 1:
                slabs_ads = self.Construct_single_adsorption()
            else:
                ele = ''.join(self.get_sites()[1:]) ### wzj 20230518
                slabs_ads = self.Construct_single_adsorption(ele=ele)
        elif self.get_sites()[0] == '2':
            slabs_ads = self.Construct_double_adsorption()
        else:
            raise ValueError('Supports only "1" "2" adsorption sites for ads!')

        if self.substrate.is_dope():
            slabs_ads = self.remove_same(slabs_ads)

        return slabs_ads

    def remove_same(self, slabs_ads):
        # To choose the config whose neighbor list includes the doped atoms
        p1 = self.substrate.property["p1"]
        p1_symb = self.substrate.property["p1_symb"]
        slabs_ads_near = []
        for slb in slabs_ads:
            (
                bind_adatoms,
                bind_adatoms_symb,
                bind_type_symb,
                adspecie,
                bind_surfatoms,
                bind_surfatoms_symb,
            ) = get_binding_adatom(slb)
            if self.get_sites() == "1" and (set(p1_symb) & set(bind_surfatoms_symb[0])):
                slabs_ads_near += [slb]
            elif (
                self.get_sites() == "2"
                and (set(p1_symb) & set(bind_surfatoms_symb[0]))
                or (set(p1_symb) & set(bind_surfatoms_symb[0]))
            ):
                slabs_ads_near += [slb]
        return slabs_ads_near

    def Construct_single_adsorption(self, ele=None):
        # generate surface adsorption configuration
        slab_ad = []
        slabs = self.substrate.construct()
        for i, slab in enumerate(slabs):
            site = AdsorptionSites(slab)
            coordinates = site.get_coordinates()
            builder = Builder(slab)
            ads_use = self.species[0].get_molecule()
            if not ele is None:
                chemical_symbols = np.array(ads_use.get_chemical_symbols())
                bond_atom_ids = chemical_symbols[chemical_symbols==ele]
                bond_atom_ids = np.where(chemical_symbols==ele)[0]
                ### print('bond_atom_ids =', bond_atom_ids, bond_atom_ids.shape)
                for j, coord in enumerate(coordinates):
                    for bond_id in bond_atom_ids:
                        slab_ad += [builder._single_adsorption(ads_use, bond=bond_id, site_index=j, direction_mode='decision_boundary')]
                        #if len(bond_atom_ids) > 1:
                        #    slab_ad += [builder._single_adsorption(ads_use, bond=bond_id, site_index=j, direction_mode='decision_boundary', direction_args=bond_atom_ids)]
            else:
                for j, coord in enumerate(coordinates):
                    slab_ad += [builder._single_adsorption(ads_use, bond=0, site_index=j)]
        return slab_ad

    def Construct_double_adsorption(self):
        slab_ad = []
        slabs = self.substrate.construct()
        for i, slab in enumerate(slabs):
            site = AdsorptionSites(slab)
            builder = Builder(slab)
            ads_use = self.species[0].get_molecule()
            edges = site.get_adsorption_edges()
            for j, edge01 in enumerate(edges):
                slab_ad += [builder._double_adsorption(ads_use, bonds=[0, 1], edge_index=j)]
        return slab_ad

    @classmethod
    def from_input(cls, init_list, substrates, species_dict=None):
        ads = []
        for i in init_list:
            spec1 = init_from_ads(i[0], species_dict)
            sites1 = str(i[1])
            for j in substrates:
                ads.append(cls([spec1], list(sites1), substrate=j))
        return ads


class Coadsorption(Adsorption):
    def __init__(self, species: list, sites: list, spec_ads_stable=None, substrate=Slab()):
        super().__init__(species, sites, spec_ads_stable, substrate)
        assert len(species) == 2, "Coads need Two adsorption Species, but %d was given" % len(
            species
        )

    def construct(self):
        if self.get_sites() == "1 1":
            slabs_ads = self.Construct_coadsorption_11()
        elif self.get_sites() == "1 2":
            slabs_ads = self.Construct_coadsorption_12()
        elif self.get_sites() == "2 2":
            slabs_ads = self.Construct_coadsorption_22()
        else:
            raise ValueError('Supports only "1 1" "1 2" "2 2" adsorption sites for coads!')
        if self.substrate.is_dope():
            slabs_ads = self.remove_same(slabs_ads)
        return slabs_ads

    def out_file_name(self):
        ads = []
        for every_species in self.species:
            ads.append(every_species.out_file_name())
        ads_str = "_".join(ads)
        substrate_str = self.substrate.out_file_name()
        vasp_file_str = "_".join([substrate_str, ads_str])
        return vasp_file_str

    def remove_same(self, slabs_ads):
        # To choose the config whose neighbor list includes the doped atoms
        p1 = self.substrate.property["p1"]
        p1_symb = self.substrate.property["p1_symb"]
        slabs_ads_near = []
        for slb in slabs_ads:
            (
                bind_adatoms,
                bind_adatoms_symb,
                bind_type_symb,
                adspecie,
                bind_surfatoms,
                bind_surfatoms_symb,
            ) = get_binding_adatom(slb)
            bind_surfatoms_symb_all = sum(bind_surfatoms_symb, [])
            if set(p1_symb) & set(bind_surfatoms_symb_all):
                slabs_ads_near += [slb]
        return slabs_ads_near

    def Construct_coadsorption_11(self):
        slab_ad = []
        ads_type = self.spec_ads_stable
        dis_inter = self.substrate.get_dis_inter()
        slabs = self.substrate.construct()
        for i, slab in enumerate(slabs):
            site01 = AdsorptionSites(slab)
            builder01 = Builder(slab)
            coordinate01 = site01.get_coordinates()
            # generate surface adsorption configuration
            ads1_use = self.species[0].get_molecule()
            ads2_use = self.species[1].get_molecule()
            for k, sitetype in enumerate(site01.get_symmetric_sites()):
                slab = builder01._single_adsorption(
                    ads1_use, bond=0, site_index=k, auto_construct=True
                )
                coord01 = site01.get_coordinates()[k]
                site02 = AdsorptionSites(slab)
                coordinates02 = site02.get_coordinates()
                for j, coord02 in enumerate(coordinates02):
                    dis = np.linalg.norm(coord01 - coord02)
                    if dis < float(dis_inter[0]):
                        continue
                    elif dis > float(dis_inter[1]):
                        continue
                    else:
                        builder02 = Builder(slab)
                        slab_ad += [
                            builder02._single_adsorption(
                                ads2_use, bond=0, site_index=j, auto_construct=True
                            )
                        ]

        typ = {None: 0, "top": 1, "bri": 2, "fcc": 3, "hcp": 3, "4-fold": 4}
        # view(slab_ad)
        slab_ad_final = []
        for j, adslab in enumerate(slab_ad):
            (
                bind_adatoms,
                bind_adatoms_symb,
                adspecie,
                bind_type_symb,
                bind_surfatoms,
                bind_surfatoms_symb,
            ) = get_binding_adatom(adslab)
            adspecie_tmp, bind_type_symb_tmp = [], []
            for k, spe in enumerate(adspecie):
                if spe in ads_type.keys():
                    adspecie_tmp += [spe]
                    bind_type_symb_tmp += [bind_type_symb[k]]
            if len(adspecie_tmp) < 2:
                # print('Can not identify the config!')
                slab_ad_final += [adslab]
            elif typ.get(bind_type_symb_tmp[0]) in ads_type.get(adspecie_tmp[0]) and typ.get(
                bind_type_symb_tmp[1]
            ) in ads_type.get(adspecie_tmp[1]):
                slab_ad_final += [adslab]
        return slab_ad_final

    def Construct_coadsorption_12(self):
        slab_ad = []
        slabs = self.substrate.construct()
        dis_inter = self.substrate.get_dis_inter()
        for i, slab in enumerate(slabs):
            site01 = AdsorptionSites(slab)
            # print(site01.get_symmetric_sites())
            builder01 = Builder(slab)
            coordinate01 = site01.get_coordinates()
            # generate surface adsorption configuration
            ads1_use = self.species[0].get_molecule()
            ads2_use = self.species[1].get_molecule()
            for k, coord01 in enumerate(coordinate01):
                slab = builder01._single_adsorption(ads1_use, bond=0, site_index=k)
                # after adsorbing an atoms
                # site analysis and surface builder
                site02 = AdsorptionSites(slab)
                builder02 = Builder(slab)
                # obtain the edges and ID and coordinates of all sites
                edge02 = site02.get_adsorption_edges()
                site_coord02 = site02.get_coordinates(unique=False)
                site_type02 = site02.get_periodic_sites(screen=True)
                dic_site = {}
                keys = [site_type02[i] for i in range(len(site_type02))]
                values = [site_coord02[i] for i in range(len(site_type02))]
                dic_site = dict(zip(keys, values))
                # emiliate the too near site
                for j, edge in enumerate(edge02):
                    coord10 = dic_site.get(edge[0])
                    coord11 = dic_site.get(edge[1])
                    if coord10 is not None:
                        dis1 = np.linalg.norm(coord01 - coord10)
                    else:
                        dis1 = dis_inter[0] + 0.1
                    if coord11 is not None:
                        dis2 = np.linalg.norm(coord01 - coord11)
                    else:
                        dis2 = dis_inter[1] + 0.1
                    dis = min(dis1, dis2)

                    if dis < dis_inter[0]:
                        continue
                    elif dis > dis_inter[1]:
                        continue
                    else:
                        slab_ad += [
                            builder02._double_adsorption(ads2_use, bonds=[0, 1], edge_index=j)
                        ]
        return slab_ad

    def Construct_coadsorption_22(self):
        slab_ad = []
        dis_inter = self.substrate.get_dis_inter()
        slabs = self.substrate.construct()
        for i, slab in enumerate(slabs):
            site01 = AdsorptionSites(slab)
            # print(site01.get_symmetric_sites())
            builder01 = Builder(slab)
            # coordinate01 = site01.get_coordinates()
            edge01 = site01.get_adsorption_edges()
            site_coord01 = site01.get_coordinates(unique=False)
            site_type01 = site01.get_periodic_sites(screen=True)
            dic_site01 = {}
            keys = [site_type01[i] for i in range(len(site_type01))]
            values = [site_coord01[i] for i in range(len(site_type01))]
            dic_site01 = dict(zip(keys, values))
            # generate surface adsorption configuration
            ads1_use = self.species[0].get_molecule()
            ads2_use = self.species[1].get_molecule()
            for k, edge01 in enumerate(edge01):
                slab = builder01._double_adsorption(ads1_use, bonds=[0, 1], edge_index=k)
                coord00 = dic_site01.get(edge01[0])
                coord01 = dic_site01.get(edge01[1])
                ## after adsorbing an atoms
                # site analysis and surface builder
                site02 = AdsorptionSites(slab)
                builder02 = Builder(slab)
                # obtain the edges and ID and coordinates of all sites
                edge02 = site02.get_adsorption_edges()
                site_coord02 = site02.get_coordinates(unique=False)
                site_type02 = site02.get_periodic_sites(screen=True)
                dic_site02 = {}
                keys = [site_type02[i] for i in range(len(site_type02))]
                values = [site_coord02[i] for i in range(len(site_type02))]
                dic_site02 = dict(zip(keys, values))
                ## emiliate the too near site
                for j, edge in enumerate(edge02):
                    coord10 = dic_site02.get(edge[0])
                    coord11 = dic_site02.get(edge[1])
                    if not coord10 is None:
                        dis1 = np.linalg.norm(coord01 - coord10)
                    else:
                        dis1 = dis_inter[0] + 0.1
                    if not coord11 is None:
                        dis2 = math.hypot(
                            coord00[0] - coord11[0],
                            coord00[1] - coord11[1],
                            coord00[2] - coord11[2],
                        )
                    else:
                        dis2 = dis_inter[1] + 0.1
                    dis = min(dis1, dis2)

                    if dis < dis_inter[0]:
                        continue
                    elif dis > dis_inter[1]:
                        continue
                    else:
                        slab_ad += [
                            builder02._double_adsorption(ads2_use, bonds=[0, 1], edge_index=j)
                        ]
        return slab_ad

    @classmethod
    def from_input(cls, init_list, substrates, species_dict=None):
        ads = []
        for i in init_list:
            spec1 = init_from_ads(i[0], species_dict)
            spec2 = init_from_ads(i[1], species_dict)
            sites1 = str(i[2])
            sites2 = str(i[3])
            for j in substrates:
                ads.append(cls([spec1, spec2], [sites1, sites2], substrate=j))
        return ads


def ads_from_input(ads_model, substrate, species_dict=None):
    ads = []
    new_ads = []
    ads_type_list = ["ads", "coads"]
    for key, value in ads_model.items():
        if key == "coads":
            new_ads = Coadsorption.from_input(value, substrate, species_dict)
        elif key == "ads":
            new_ads = Adsorption.from_input(value, substrate, species_dict)
        else:
            msg = ",".join(ads_type_list)
            warn_msg = (
                "Only support species type: %s, Your input %s part in Species will be dismiss"
                % (msg, key)
            )
            raise Warning(warn_msg)
        ads = ads + new_ads
    return ads
