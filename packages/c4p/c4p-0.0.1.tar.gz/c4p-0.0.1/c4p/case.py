import os
from . import utils

class PaleoCase:
    def __init__(self, casename=None, work_dirpath=None):
        self.casename = casename
        self.work_dirpath = work_dirpath
        if not os.path.exists(work_dirpath):
            os.makedirs(work_dirpath, exist_ok=True)
            utils.p_success(f'>>> {work_dirpath} created')
        os.chdir(work_dirpath)
        utils.p_success(f'>>> Current directory switched to: {work_dirpath}')

        
    def setup_rtm(self, topo_path, ocn_scrp_path, grids_dirpath,
                  url_create_topo_ncl='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/create-topo_1x1deg.ncl',
                  url_rdirc_template_csh='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/rdirc_template.csh',
                  url_topo2rdirc_sed_f90='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/topo2rdirc_sed.F90',
                  url_Makefile='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/Makefile',
                  url_plotrdirc_csh='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/plotrdirc.csh',
                  url_plotrdirc_ncl='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/plot_rdirc.ncl',
                  url_rtm_ncdf_pro='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/rtm_ncdf.pro',
                  url_runoff_map='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/runoff_map_1deg',
                  url_runoff_map_template_nml='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/runoff_map.1x1.template.nml',
                  url_create_ESMF_map_sh='https://github.com/CESM-Development/paleoToolkit/trunk/cesm1_2/rof/create_ESMF_map.sh',
                  ):
        # Step 19
        fpath = utils.svn_export(url_create_topo_ncl)
        utils.replace_str(
            fpath,
            {
                '<casename>': self.casename,
                '<input_topo-bath_filename>': topo_path,
            },
        )
        utils.run_shell(f'ncl {fpath}', timeout=3)
        
        # Step 20
        fpath_new = utils.svn_export(url_rdirc_template_csh, f'./rdirc_{self.casename}.csh')
        utils.replace_str(
            fpath_new,
            {
                '<casename>': self.casename,
                '<path/topography-bathymetry_file>': f'topo.1x1deg.{self.casename}.nc',
            },
        )

        fpath = utils.svn_export(url_topo2rdirc_sed_f90)
        utils.replace_str(
            fpath,
            {
                'pause': 'WRITE(*, *)',  # to avoid the prompts
            },
        )

        utils.svn_export(url_Makefile)
        utils.exec_script(fpath_new)

        # Step 21
        fpath = utils.svn_export(url_plotrdirc_csh)
        utils.replace_str(
            fpath,
            {
                '<casename>': self.casename,
                '<topography-bathymetry_file>': os.path.basename(topo_path),
            },
        )
        fpath_ncl = utils.svn_export(url_plotrdirc_ncl)

        # output png instead of ps
        utils.replace_str(
            fpath_ncl,
            {
                'PSName= "ps"': 'PSName= "png"',
            },
        )

        utils.exec_script(fpath)

        # Step 24
        fpath = utils.svn_export(url_rtm_ncdf_pro)
        
        utils.replace_str(
            fpath,
            {
                '<casename>': self.casename,
                '<user>': 'Feng Zhu',
                '<date>': '20230514',
                "if !d.name eq 'X' then device, decomp=0": ";if !d.name eq 'X' then device, decomp=0",  # so that Xwindows is not required
            },
        )

        # run IDL
        utils.run_shell('source /glade/u/apps/ch/opt/lmod/8.7.13/lmod/lmod/init/zsh && module load idl && printf ".rn rtm_ncdf\nrtm\nexit\n" | idl')

        # Step 25
        fpath = utils.svn_export(url_runoff_map)
        fpath_new = utils.svn_export(url_runoff_map_template_nml,  f'./runoff_map.1x1.{self.casename}.nml')
        utils.replace_str(
            fpath_new,
            {
                '<casename>': self.casename,
                './<SCRIP_mapping_file>': ocn_scrp_path,
                '<ocnres>': 'gx1Miocene',
                '<date>': '20230514',
            },
        )
        utils.run_shell(f'ln -s {fpath_new} ./runoff_map.nml')
        utils.exec_script(fpath)

        # Step 26
        fpath = utils.svn_export(url_create_ESMF_map_sh)
        ocnres = f'gx1{self.casename}'
        fsrc = os.path.join(grids_dirpath, '1x1d.nc')
        fdst = ocn_scrp_path
        utils.exec_script(fpath, args=f'-fsrc {fsrc} -nsrc r1_nomask -fdst {fdst} -ndst {ocnres} -map aave')

        # Step 27
        fsrc = os.path.join(grids_dirpath, 'fv1.9x2.5_141008.nc')
        fdst = os.path.join(grids_dirpath, '1x1d_lonshift.nc')
        utils.exec_script(fpath, args=f'-fsrc {fsrc} -nsrc r19_nomask -fdst {fdst} -ndst r1x1 -map aave')

        fsrc = os.path.join(grids_dirpath, '1x1d_lonshift.nc')
        fdst = os.path.join(grids_dirpath, 'fv1.9x2.5_141008.nc')
        utils.exec_script(fpath, args=f' -fsrc {fsrc} -nsrc r1x1 -fdst {fdst} -ndst r19 -map aave')