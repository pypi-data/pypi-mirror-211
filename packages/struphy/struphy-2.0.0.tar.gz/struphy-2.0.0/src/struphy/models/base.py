from abc import ABCMeta, abstractmethod
import numpy as np


class StruphyModel(metaclass=ABCMeta):
    """
    Base class for all Struphy models.

    Parameters
    ----------
    params : dict
        Simulation parameters, see from :ref:`params_yml`.

    comm : mpi4py.MPI.Intracomm
        MPI communicator for parallel runs.

    species : dict
        The dynamical fields and kinetic species of the model. 

        Keys are either:

        a) the electromagnetic field/potential names (b_field=, e_field=) 
        b) the fluid species names (e.g. mhd=)
        c) the names of the kinetic species (e.g. electrons=, energetic_ions=)

        Corresponding values are:

        a) a space ID ("H1", "Hcurl", "Hdiv", "L2" or "H1vec"),
        b) a dict with key=variable_name (e.g. n, U, p, ...) and value=space ID ("H1", "Hcurl", "Hdiv", "L2" or "H1vec"),
        c) the type of particles ("Particles6D", "Particles5D", ...).

    Note
    ----
    All Struphy models are subclasses of ``StruphyModel`` and should be added to ``struphy/models/models.py``.  
    """

    def __init__(self, params, comm, **species):

        from struphy.models.utilities import setup_domain_mhd, setup_electric_background, setup_derham
        from struphy.psydac_api.mass import WeightedMassOperators

        self._params = params
        self._comm = comm
        self._species = species

        # initialize model variable dictionaries
        self._init_variable_dicts()

        # compute model units
        self._units_basic, self._units_der, self._units_dimless = self.model_units(
            self.params, verbose=False)

        # create domain, MHD equilibrium, background electric field
        self._domain, self._mhd_equil = setup_domain_mhd(params)
        self._electric_equil = setup_electric_background(params, self.domain)

        # create discrete derham sequence
        dims_mask = params['grid']['dims_mask']
        if dims_mask is None:
            dims_mask = [True]*3

        self._derham = setup_derham(
            params['grid'], comm=comm, domain=self.domain, mpi_dims_mask=dims_mask)

        # create weighted mass operators
        self._mass_ops = WeightedMassOperators(
            self.derham, self.domain, eq_mhd=self.mhd_equil)

        # allocate memory for variables
        self._allocate_variables()

    @classmethod
    @abstractmethod
    def bulk_species(cls):
        '''Object identifying the bulk species of the plasma. Must be a value of self.fluid or self.kinetic, or None.'''
        pass

    @classmethod
    @abstractmethod
    def timescale(cls):
        '''String that sets the time scale unit of the model. 
        Must be one of "alfvén", "cyclotron" or "light".'''
        pass

    @property
    @abstractmethod
    def propagators(self):
        '''List of :ref:`propagators` used in the time stepping of the model.'''
        pass

    @property
    @abstractmethod
    def scalar_quantities(self):
        '''Dictionary of scalar quantities to be saved during simulation. 
        Must be initialized as empty np.array of size 1::

        The time series self._scalar_quantities['time'] = np.empty(1, dtype=float) must be contained.'''
        pass

    @abstractmethod
    def update_scalar_quantities(self):
        ''' Specify an update rule for each item in scalar_quantities.
        '''
        pass

    @property
    def params(self):
        '''Model parameters from :code:`parameters.yml`.'''
        return self._params

    @property
    def comm(self):
        '''MPI communicator.'''
        return self._comm

    @property
    def species(self):
        '''Species dictionary.'''
        return self._species

    @property
    def em_fields(self):
        '''Dictionary of electromagnetic field/potential variables.'''
        return self._em_fields

    @property
    def fluid(self):
        '''Dictionary of fluid species.'''
        return self._fluid

    @property
    def kinetic(self):
        '''Dictionary of kinetic species.'''
        return self._kinetic

    @property
    def domain(self):
        '''Domain object, see :ref:`avail_mappings`.'''
        return self._domain

    @property
    def mhd_equil(self):
        '''MHD equilibrium object, see :ref:`mhd_equil`.'''
        return self._mhd_equil

    @property
    def electric_equil(self):
        '''Eelctric equilibrium object, see :ref:`electric_equil`.'''
        return self._electric_equil

    @property
    def derham(self):
        '''3d Derham sequence, see :ref:`derham`.'''
        return self._derham

    @property
    def units_basic(self):
        '''Basic units of the model.
        '''
        return self._units_basic

    @property
    def units_der(self):
        '''Derived units of the model.
        '''
        return self._units_der

    @property
    def units_dimless(self):
        '''Dimensionless qunatities of the model.
        '''
        return self._units_dimless

    @property
    def mass_ops(self):
        '''WeighteMassOperators object, see :ref:`mass_ops`.'''
        return self._mass_ops

    def integrate(self, dt, split_algo='LieTrotter'):
        """
        Advance the model by a time step dt.

        Parameters
        ----------
        dt : float
            Time step of time integration.

        split_algo : str
            Splitting algorithm. Currently available: "LieTrotter" and "Strang".
        """

        # first order in time
        if split_algo == 'LieTrotter':

            for propagator in self.propagators:
                propagator(dt)

        # second order in time
        elif split_algo == 'Strang':

            assert len(self.propagators) > 1

            for propagator in self.propagators:
                propagator(dt/2)

            for propagator in self.propagators[::-1]:
                propagator(dt/2)

        else:
            raise NotImplementedError(
                f'Splitting scheme {split_algo} not available.')

    def update_markers_to_be_saved(self):
        '''
        Writes markers with IDs that are supposed to be saved into corresponding array.
        '''

        for val in self.kinetic.values():

            n_mks_save = val['params']['save_data']['n_markers']
            if n_mks_save > 0:
                markers_on_proc = np.logical_and(
                    val['obj'].markers[:, -1] >= 0., val['obj'].markers[:, -1] < n_mks_save)
                n_markers_on_proc = np.count_nonzero(markers_on_proc)
                val['kinetic_data']['markers'][:] = -1.
                val['kinetic_data']['markers'][:n_markers_on_proc] = val['obj'].markers[markers_on_proc]

    def update_distr_function(self):
        '''
        Writes distribution function slices that are supposed to be saved into corresponding array.
        '''

        dim_to_int = {'e1': 0, 'e2': 1, 'e3': 2, 'v1': 3, 'v2': 4, 'v3': 5}

        for val in self.kinetic.values():

            if 'f' in val['params']['save_data']:

                for slice_i, edges in val['bin_edges'].items():

                    dims = (len(slice_i) - 2)//3 + 1
                    comps = [slice_i[3*i:3*i + 2] for i in range(dims)]
                    components = [False]*6

                    for comp in comps:
                        components[dim_to_int[comp]] = True

                    val['kinetic_data']['f'][slice_i][:] = val['obj'].binning(
                        components, edges, self.domain)

    def print_scalar_quantities(self):
        '''
        Print quantities saved in scalar_quantities to screen.
        '''
        sq_str = ''
        for key, val in self._scalar_quantities.items():
            sq_str += key + ': {:15.11f}'.format(val[0]) + '     '
        print(sq_str)

    def initialize_from_params(self):
        """
        Set initial conditions for FE coefficients (electromagnetic and fluid) and markers according to parameter file.
        """

        # initialize em fields
        if len(self.em_fields) > 0:

            for key, val in self.em_fields.items():
                if 'params' not in key:
                    val['obj'].initialize_coeffs(
                        self.em_fields['params']['init'], domain=self.domain)

        # initialize fields
        if len(self.fluid) > 0:

            for val in self.fluid.values():

                for variable, subval in val.items():
                    if 'params' not in variable:
                        subval['obj'].initialize_coeffs(
                            val['params']['init'], domain=self.domain)

        # initialize particles
        if len(self.kinetic) > 0:

            for val in self.kinetic.values():
                val['obj'].mpi_sort_markers(do_test=True)

                typ = val['params']['markers']['type']
                if typ == 'full_f':
                    val['obj'].initialize_weights(val['params']['init'])
                elif typ == 'delta_f':
                    val['obj'].initialize_weights(val['params']['init'])
                elif typ == 'control_variate':
                    val['obj'].initialize_weights(
                        val['params']['init'], val['params']['background'])
                else:
                    raise NotImplementedError(
                        f'Type {typ} for distribution function is not known!')

                if val['space'] == 'Particles5D':
                    val['obj'].save_magnetic_moment(self.derham)

    def initialize_from_restart(self, data):
        """
        Set initial conditions for FE coefficients (electromagnetic and fluid) and markers from restart group in hdf5 files.

        Parameters
        ----------
        data : struphy.models.output_handling.DataContainer
            The data object that links to the hdf5 files.
        """

        # initialize em fields
        if len(self.em_fields) > 0:

            for key, val in self.em_fields.items():
                if 'params' not in key:
                    val['obj'].initialize_coeffs_from_restart_file(data.file)

        # initialize fields
        if len(self.fluid) > 0:

            for species, val in self.fluid.items():

                for variable, subval in val.items():
                    if 'params' not in variable:
                        subval['obj'].initialize_coeffs_from_restart_file(
                            data.file, species)

        # initialize particles
        if len(self.kinetic) > 0:

            for key, val in self.kinetic.items():
                val['obj']._markers[:, :] = data.file['restart/' + key][-1, :, :]

                # important: sets holes attribute of markers!
                val['obj'].mpi_sort_markers(do_test=True)

    def initialize_data_output(self, data, size):
        """
        Create datasets in hdf5 files according to model unknowns and diagnostics data.

        Parameters
        ----------
        data : struphy.models.output_handling.DataContainer
            The data object that links to the hdf5 files.

        size : int
            Number of MPI processes of the model run.

        Returns
        -------
        save_keys_all : list
            Keys of datasets which are saved during the simulation.

        save_keys_end : list
            Keys of datasets which are saved at the end of a simulation to enable restarts.
        """

        from psydac.linalg.stencil import StencilVector

        # save scalar quantities in group 'scalar/'
        for key, val in self.scalar_quantities.items():
            key_scalar = 'scalar/' + key
            data.add_data({key_scalar: val})

        # store grid_info only for runs with 512 ranks or smaller
        if size <= 512:
            data.file['scalar'].attrs['grid_info'] = self.derham.domain_array
        else:
            data.file['scalar'].attrs['grid_info'] = self.derham.domain_array[0]

        # save electromagentic fields/potentials data in group 'feec/'
        for key, val in self.em_fields.items():
            if 'params' not in key:
                key_field = 'feec/' + key
                key_field_restart = 'restart/' + key

                # in-place extraction of FEM coefficients from field.vector --> field.vector_stencil!
                val['obj'].extract_coeffs(update_ghost_regions=False)

                # save numpy array to be updated each time step.
                if isinstance(val['obj'].vector_stencil, StencilVector):
                    data.add_data({key_field: val['obj'].vector_stencil._data})
                    data.add_data(
                        {key_field_restart: val['obj'].vector_stencil._data})
                else:
                    for n in range(3):
                        key_component = key_field + '/' + str(n + 1)
                        key_component_restart = key_field_restart + \
                            '/' + str(n + 1)
                        data.add_data(
                            {key_component: val['obj'].vector_stencil[n]._data})
                        data.add_data(
                            {key_component_restart: val['obj'].vector_stencil[n]._data})

                # save field meta data
                data.file[key_field].attrs['space_id'] = val['obj'].space_id
                data.file[key_field].attrs['starts'] = val['obj'].starts
                data.file[key_field].attrs['ends'] = val['obj'].ends
                data.file[key_field].attrs['pads'] = val['obj'].pads

        # save fluid data in group 'feec/'
        for species, val in self.fluid.items():

            species_path = 'feec/' + species + '_'
            species_path_restart = 'restart/' + species + '_'

            for variable, subval in val.items():
                if 'params' not in variable:
                    key_field = species_path + variable
                    key_field_restart = species_path_restart + variable

                    # in-place extraction of FEM coefficients from field.vector --> field.vector_stencil!
                    subval['obj'].extract_coeffs(update_ghost_regions=False)

                    # save numpy array to be updated each time step.
                    if isinstance(subval['obj'].vector_stencil, StencilVector):
                        data.add_data(
                            {key_field: subval['obj'].vector_stencil._data})
                        data.add_data(
                            {key_field_restart: subval['obj'].vector_stencil._data})
                    else:
                        for n in range(3):
                            key_component = key_field + '/' + str(n + 1)
                            key_component_restart = key_field_restart + \
                                '/' + str(n + 1)
                            data.add_data(
                                {key_component: subval['obj'].vector_stencil[n]._data})
                            data.add_data(
                                {key_component_restart: subval['obj'].vector_stencil[n]._data})

                    # save field meta data
                    data.file[key_field].attrs['space_id'] = subval['obj'].space_id
                    data.file[key_field].attrs['starts'] = subval['obj'].starts
                    data.file[key_field].attrs['ends'] = subval['obj'].ends
                    data.file[key_field].attrs['pads'] = subval['obj'].pads

        # save kinetic data in group 'kinetic/'
        for key, val in self.kinetic.items():
            key_spec = 'kinetic/' + key
            key_spec_restart = 'restart/' + key

            data.add_data({key_spec_restart: val['obj']._markers})

            for key1, val1 in val['kinetic_data'].items():
                key_dat = key_spec + '/' + key1

                if isinstance(val1, dict):
                    for key2, val2 in val1.items():
                        key_f = key_dat + '/' + key2
                        data.add_data({key_f: val2})

                        dims = (len(key2) - 2)//3 + 1
                        for dim in range(dims):
                            data.file[key_f].attrs['bin_centers' + '_' + str(dim + 1)] = val['bin_edges'][key2][dim][:-1] + (
                                val['bin_edges'][key2][dim][1] - val['bin_edges'][key2][dim][0])/2

                else:
                    data.add_data({key_dat: val1})

        # keys to be saved at each time step and only at end (restart)
        save_keys_all = []
        save_keys_end = []

        for key in data.dset_dict:
            if 'restart' in key:
                save_keys_end.append(key)
            else:
                save_keys_all.append(key)

        return save_keys_all, save_keys_end

    ###################
    # Class methods :
    ###################

    @classmethod
    def model_units(cls, params, verbose=False):
        """
        Compute model units and print them to screen.

        Parameters
        ----------
        params : dict
            model parameters.

        verbose : bool, optional
            print model units to screen.
        """

        from struphy.models.utilities import derive_units

        x_unit = params['units']['x']
        B_unit = params['units']['B']

        if verbose:
            print('\nNumerical values of variables are expressed in the following units:')
            print(f'Unit of length:'.ljust(25),
                  '{:4.3e}'.format(x_unit) + ' m')

        # special case for model Maxwell (no plasma species)
        if cls.bulk_species() is None:
            if verbose:
                print(f'Unit of time:'.ljust(25),
                      '{:4.3e}'.format(x_unit / 299792458) + ' s')
                print(f'Unit of velocity:'.ljust(25),
                      '{:4.3e}'.format(299792458) + ' m/s')
                print(f'Unit of magnetic field:'.ljust(
                    25), '{:4.3e}'.format(B_unit) + ' T')
                print(f'Unit of electric field:'.ljust(25),
                      '{:4.3e}'.format(299792458*B_unit) + ' V/m')

            units_basic = {}
            units_basic['t'] = x_unit / 299792458
            units_basic['x'] = x_unit
            units_basic['B'] = B_unit

            return units_basic, {}, {}
        else:

            # look for bulk species in fluid OR kinetic parameter dictionaries
            if 'fluid' in params:
                if cls.bulk_species() in params['fluid']:
                    Z_bulk = params['fluid'][cls.bulk_species()
                                             ]['phys_params']['Z']
                    A_bulk = params['fluid'][cls.bulk_species()
                                             ]['phys_params']['A']
            else:
                Z_bulk = params['kinetic'][cls.bulk_species()
                                           ]['phys_params']['Z']
                A_bulk = params['kinetic'][cls.bulk_species()
                                           ]['phys_params']['A']

            # compute units
            units_basic, units_der, units_dimless = derive_units(
                Z_bulk, A_bulk, params['units']['x'], params['units']['B'], params['units']['n'], cls.timescale())

            if verbose:
                print(f'Unit of time:'.ljust(25),
                      '{:4.3e}'.format(units_basic['t']) + ' s')
                print(f'Unit of velocity:'.ljust(25),
                      '{:4.3e}'.format(units_der['v']) + ' m/s')
                print(f'Unit of magnetic field:'.ljust(25),
                      '{:4.3e}'.format(units_basic['B']) + ' T')
                print(f'Unit of particle density:'.ljust(25),
                      '{:4.3e}'.format(units_der['n']) + ' m⁻³')
                print(f'Unit of mass:'.ljust(25),
                      '{:4.3e}'.format(units_basic['m']) + ' kg')
                print(f'Unit of mass density:'.ljust(25),
                      '{:4.3e}'.format(units_der['rho']) + ' kg/m³')
                print(f'Unit of pressure:'.ljust(25),
                      '{:4.3e}'.format(units_der['p'] * 1e-5) + ' bar')

                # dimensionless quantities
                print('\nRelevant dimensionless quantities:')
                print(f'alpha:'.ljust(25), '{:7.3f}'.format(
                    units_dimless['alpha']))
                print(f'kappa:'.ljust(25), '{:7.3f}'.format(
                    units_dimless['kappa']))

            return units_basic, units_der, units_dimless

    ###################
    # Private methods :
    ###################

    def _init_variable_dicts(self):
        """
        Initialize em-fields, fluid and kinetic dictionaries for information on the model variables.
        """

        # electromagnetic fields, fluid and/or kinetic species
        self._em_fields = {}
        self._fluid = {}
        self._kinetic = {}

        # create dictionaries for each em-field/species and fill in space/class name and parameters
        for var_name, space in self.species.items():

            if isinstance(space, str):

                if space in {'H1', 'Hcurl', 'Hdiv', 'L2', 'H1vec'}:

                    assert 'em_fields' in self.params, 'Top-level key "em_fields" is missing in parameter file.'
                    self._em_fields[var_name] = {}
                    self._em_fields[var_name]['space'] = space
                    self._em_fields['params'] = self.params['em_fields']

                elif space in {'Particles6D', 'Particles5D'}:

                    assert 'kinetic' in self.params, 'Top-level key "kinetic" is missing in parameter file.'
                    assert var_name in self.params[
                        'kinetic'], f'Kinetic species {var_name} is missing in parameter file.'

                    self._kinetic[var_name] = {}
                    self._kinetic[var_name]['space'] = space
                    self._kinetic[var_name]['params'] = self.params['kinetic'][var_name]

                else:
                    raise ValueError(
                        f'The given value string {space} is not supported!')

            elif isinstance(space, dict):

                assert 'fluid' in self.params, 'Top-level key "fluid" is missing in parameter file.'
                assert var_name in self.params[
                    'fluid'], f'Fluid species {var_name} is missing in parameter file.'

                self._fluid[var_name] = {}

                for sub_var_name, sub_space in space.items():
                    self._fluid[var_name][sub_var_name] = {}
                    self._fluid[var_name][sub_var_name]['space'] = sub_space

                self._fluid[var_name]['params'] = self.params['fluid'][var_name]

            else:
                raise ValueError(f'Type {type(space)} not supported as value.')

    def _allocate_variables(self):
        """
        Allocate memory for model variables. 
        Creates FEM fields for em-fields and fluid variables and a particle class for kinetic species.
        """

        from struphy.psydac_api.fields import Field
        from struphy.pic import particles

        # allocate memory for FE coeffs of electromagnetic fields/potentials
        if 'em_fields' in self.params:

            for key, val in self.em_fields.items():

                if 'params' not in key:
                    val['obj'] = Field(key, val['space'], self.derham)

        # allocate memory for FE coeffs of fluid variables
        if 'fluid' in self.params:

            for species, val in self.fluid.items():

                for variable, subval in val.items():

                    if 'params' not in variable:
                        subval['obj'] = Field(
                            variable, subval['space'], self.derham)

        # marker arrays and plasma parameters of kinetic species
        if 'kinetic' in self.params:

            for species, val in self.kinetic.items():

                if self.params['kinetic'][species]['markers']['type'] in ['control_variate', 'delta_f']:
                    assert 'background' in self.params['kinetic'][species], \
                        f'If a control variate or delta-f method is used, a analytical background must be given!'

                kinetic_class = getattr(particles, val['space'])

                val['obj'] = kinetic_class(species,
                                           **val['params']['phys_params'],
                                           **val['params']['markers'],
                                           comm=self.derham.comm,
                                           domain_array=self.derham.domain_array,
                                           domain=self.domain,
                                           mhd_equil=self.mhd_equil,
                                           units_basic=self.units_basic)

                # for storing markers
                n_markers = val['params']['save_data']['n_markers']
                assert n_markers <= val['obj'].n_mks
                if n_markers > 0:
                    val['kinetic_data'] = {}
                    val['kinetic_data']['markers'] = np.zeros(
                        (n_markers, val['obj'].markers.shape[1]), dtype=float)

                # for storing the distribution function
                if 'f' in val['params']['save_data']:
                    slices = val['params']['save_data']['f']['slices']
                    n_bins = val['params']['save_data']['f']['n_bins']
                    ranges = val['params']['save_data']['f']['ranges']

                    val['kinetic_data']['f'] = {}
                    val['bin_edges'] = {}
                    if len(slices) > 0:
                        for i, sli in enumerate(slices):

                            assert ((len(sli) - 2)/3).is_integer()
                            val['bin_edges'][sli] = []
                            dims = (len(sli) - 2)//3 + 1
                            for j in range(dims):
                                val['bin_edges'][sli] += [np.linspace(
                                    ranges[i][j][0], ranges[i][j][1], n_bins[i][j] + 1)]
                            val['kinetic_data']['f'][sli] = np.zeros(
                                n_bins[i], dtype=float)

                # other data (wave-particle power exchange, etc.)
                # TODO

    def print_plasma_params(self):
        """
        Compute and print volume averaged plasma parameters for each species of the model.

        Global parameters:
        - plasma volume
        - transit length
        - magnetic field

        Species dependent parameters:
        - mass
        - charge
        - density
        - pressure
        - thermal energy
        - thermal speed
        - thermal frequency
        - cyclotron frequency
        - Larmor radius
        - rho/L
        - plasma frequency

        in case of MHD species
        - alfven speed
        - alfven frequency
        """

        characteristics = {}

        # physics constants
        e = 1.602176634e-19  # elementary charge (C)
        m_p = 1.67262192369e-27  # proton mass (kg)
        mu0 = 1.25663706212e-6  # magnetic constant (N*A^-2)
        eps0 = 8.8541878128e-12  # vacuum permittivity (F*m^-1)
        kB = 1.380649e-23  # Boltzmann constant (J*K^-1)

        # exit when there is not any plasma species
        if len(self.fluid) == 0 and len(self.kinetic) == 0:
            return

        # compute model units
        units_basic, units_der, unidts_dimless = self.model_units(
            self.params, verbose=False)

        # SI units
        units = {}
        units['plasma volume'] = ' m³'
        units['transit length'] = ' m'
        units['magnetic field'] = ' T'
        units['mass'] = ' kg'
        units['charge'] = ' C'
        units['density'] = ' m⁻³'
        units['pressure'] = ' bar'
        units['thermal energy'] = ' keV'
        units['thermal speed'] = ' m/s'
        units['thermal speed eta1'] = ' m/s'
        units['thermal speed eta2'] = ' m/s'
        units['thermal speed eta3'] = ' m/s'
        units['thermal frequency'] = ' MHz'
        units['cyclotron frequency'] = ' MHz'
        units['Larmor radius'] = ' m'
        units['rho/L'] = ''
        units['plasma frequency'] = ' MHz'
        units['alfvén speed'] = ' m/s'
        units['alfvén frequency'] = ' MHz'

        h = 1/20
        eta1 = np.linspace(h/2., 1.-h/2., 20)
        eta2 = np.linspace(h/2., 1.-h/2., 20)
        eta3 = np.linspace(h/2., 1.-h/2., 20)

        # global parameters
        # plasma volume (hat x^3)
        vol1 = np.mean(np.abs(self.domain.jacobian_det(eta1, eta2, eta3))) 
        # plasma volume (m⁻³)
        plasma_volume = vol1 * units_basic['x']**3
        # transit length (m)
        transit_length = plasma_volume**(1/3)
        # magnetic field (T)
        magnetic_field = np.mean(self.mhd_equil.absB0(eta1, eta2, eta3)
                                 * np.abs(self.domain.jacobian_det(eta1, eta2, eta3))) \
            / vol1 * units_basic['B']

        print('\nGlobal characteristics of the simulation:')
        print(f'Plasma volume:'.ljust(25),
              '{:4.3e}'.format(plasma_volume) + units['plasma volume'])
        print(f'Transit length:'.ljust(25),
              '{:4.3e}'.format(transit_length) + units['transit length'])
        print(f'Volume-averaged magnetic field:'.ljust(25),
              '{:4.3e}'.format(magnetic_field) + units['magnetic field'])

        # species dependent parameters
        if len(self.fluid) > 0:

            for species, val in self.fluid.items():
                characteristics[species] = {}
                # mass (kg)
                characteristics[species]['mass'] = val['params']['phys_params']['A']*m_p
                # charge (C)
                characteristics[species]['charge'] = val['params']['phys_params']['Z']*e
                # density (m⁻³)
                characteristics[species]['density'] = np.mean(self.mhd_equil.n0(eta1, eta2, eta3)
                                                              * np.abs(self.domain.jacobian_det(eta1, eta2, eta3))) / plasma_volume*units_der['n']
                # pressure (bar)
                characteristics[species]['pressure'] = np.mean(self.mhd_equil.p0(eta1, eta2, eta3)
                                                               * np.abs(self.domain.jacobian_det(eta1, eta2, eta3))) / plasma_volume*units_der['p']
                # thermal energy (keV)
                characteristics[species]['thermal energy'] = characteristics[species]['pressure'] * \
                    1e5/characteristics[species]['density']/e*1e-3
                # thermal speed (m/s)
                characteristics[species]['thermal speed'] = np.sqrt(
                    characteristics[species]['thermal energy'] * 1e3 * e / characteristics[species]['mass'])
                # thermal frequency (MHz)
                characteristics[species]['thermal frequency'] = characteristics[species]['thermal speed'] / \
                    transit_length/(2*np.pi)*1e-6
                # cyclotron frequency (MHz)
                characteristics[species]['cyclotron frequency'] = characteristics[species]['charge'] * \
                    magnetic_field / \
                    characteristics[species]['mass'] / (2*np.pi) * 1e-6
                # Larmor radius (m)
                characteristics[species]['Larmor radius'] = characteristics[species]['mass'] * \
                    characteristics[species]['thermal speed'] / \
                    (characteristics[species]['charge'] * magnetic_field)
                # rho/L (unitless)
                characteristics[species]['rho/L'] = characteristics[species]['Larmor radius']/transit_length
                # plasma frequency (MHz)
                characteristics[species]['plasma frequency'] = np.sqrt(characteristics[species]['density']
                                                                       * (characteristics[species]['charge'])**2 / eps0 / characteristics[species]['mass']) / (2*np.pi) * 1e-6
                # alfvén speed (m/s)
                characteristics[species]['alfvén speed'] = magnetic_field / np.sqrt(
                    mu0 * characteristics[species]['mass'] * characteristics[species]['density'])
                # alfvén frequency (MHz)
                characteristics[species]['alfvén frequency'] = characteristics[species]['alfvén speed'] / \
                    transit_length / (2*np.pi) * 1e-6

        if len(self.kinetic) > 0:

            for species, val in self.kinetic.items():
                characteristics[species] = {}

                # mass (kg)
                characteristics[species]['mass'] = val['params']['phys_params']['A']*m_p
                # charge (C)
                characteristics[species]['charge'] = val['params']['phys_params']['Z']*e
                # density (m⁻³)
                if 'background' in val['params']:
                    type = val['params']['background']['type']
                    characteristics[species]['density'] = val['params']['background'][type]['n']*units_der['n']

                else:
                    type = val['params']['init']['type']

                    if type in val['params']['init'] and 'n' in val['params']['init'][type]:
                        characteristics[species]['density'] = val['params']['init'][type]['n']*units_der['n']

                    # When density is not specified, assume density = 1*density unit
                    else:
                        characteristics[species]['density'] = units_der['n']

                # thermal speed (m/s)
                thermal_speed = 0.
                for dir in range(val['obj'].vdim):
                    thermal_kinds = 'thermal speed eta' + str(dir + 1)
                    characteristics[species][thermal_kinds] = \
                        val['params']['markers']['loading']['moments'][dir +
                                                                       val['obj'].vdim] * units_der['v']
                    thermal_speed += characteristics[species][thermal_kinds]

                characteristics[species]['thermal speed'] = thermal_speed / \
                    val['obj'].vdim
                # thermal energy (keV)
                characteristics[species]['thermal energy'] = characteristics[species]['mass'] * \
                    characteristics[species]['thermal speed']**2 / e * 1e-3
                # pressure (bar)
                characteristics[species]['pressure'] = characteristics[species]['thermal energy'] * \
                    e*1e3*characteristics[species]['density'] * 1e-5
                # thermal frequency (MHz)
                characteristics[species]['thermal frequency'] = characteristics[species]['thermal speed'] / \
                    transit_length / (2*np.pi) * 1e-6
                # cyclotron frequency (MHz)
                characteristics[species]['cyclotron frequency'] = characteristics[species]['charge'] * \
                    magnetic_field / \
                    characteristics[species]['mass'] / (2*np.pi) * 1e-6
                # Larmor radius (m)
                characteristics[species]['Larmor radius'] = characteristics[species]['mass'] * \
                    characteristics[species]['thermal speed'] / \
                    (characteristics[species]['charge'] * magnetic_field)
                # rho/L (unitless)
                characteristics[species]['rho/L'] = characteristics[species]['Larmor radius']/transit_length
                # plasma frequency (MHz)
                characteristics[species]['plasma frequency'] = np.sqrt(characteristics[species]['density'] *
                                                                       (characteristics[species]['charge'])**2 / eps0 / characteristics[species]['mass']) / (2*np.pi) * 1e-6

        print('\nSpecies dependent characteristics of the simulation:')
        for species, ch in characteristics.items():
            print(f'\nspecies: ' + species)
            for kinds, vals in ch.items():
                print(kinds.ljust(25), '{:4.3e}'.format(vals), units[kinds])
