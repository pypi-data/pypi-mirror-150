from libc.stdint cimport int8_t, uint16_t, int64_t, uint32_t, uint64_t, uint8_t

cdef extern from "libxnvme.h":

    cdef struct xnvme_be_attr:
        char* name
        uint8_t enabled
        uint8_t _rsvd[15]

    cdef struct xnvme_be_attr_list:
        uint32_t capacity
        int count
        xnvme_be_attr item[1]

    int xnvme_be_attr_list_bundled(xnvme_be_attr_list** list)

    cdef struct xnvme_dev

    xnvme_geo* xnvme_dev_get_geo(xnvme_dev* dev)

    xnvme_spec_idfy_ctrlr* xnvme_dev_get_ctrlr(xnvme_dev* dev)

    xnvme_spec_idfy_ctrlr* xnvme_dev_get_ctrlr_css(xnvme_dev* dev)

    xnvme_spec_idfy_ns* xnvme_dev_get_ns(xnvme_dev* dev)

    xnvme_spec_idfy_ns* xnvme_dev_get_ns_css(xnvme_dev* dev)

    uint32_t xnvme_dev_get_nsid(xnvme_dev* dev)

    uint8_t xnvme_dev_get_csi(xnvme_dev* dev)

    xnvme_ident* xnvme_dev_get_ident(xnvme_dev* dev)

    void* xnvme_dev_get_be_state(xnvme_dev* dev)

    uint64_t xnvme_dev_get_ssw(xnvme_dev* dev)

    void* xnvme_buf_phys_alloc(xnvme_dev* dev, size_t nbytes, uint64_t* phys)

    void xnvme_buf_phys_free(xnvme_dev* dev, void* buf)

    void* xnvme_buf_phys_realloc(xnvme_dev* dev, void* buf, size_t nbytes, uint64_t* phys)

    int xnvme_buf_vtophys(xnvme_dev* dev, void* buf, uint64_t* phys)

    void* xnvme_buf_virt_alloc(size_t alignment, size_t nbytes)

    void xnvme_buf_virt_free(void* buf)

    uint64_t XNVME_ILOG2(uint64_t x)

    int XNVME_MIN(int x, int y)

    uint64_t XNVME_MIN_U64(uint64_t x, uint64_t y)

    int64_t XNVME_MIN_S64(int64_t x, int64_t y)

    int XNVME_MAX(int x, int y)

    uint64_t _xnvme_timer_clock_sample()

    cdef struct xnvme_timer:
        uint64_t start
        uint64_t stop

    uint64_t xnvme_timer_start(xnvme_timer* t)

    uint64_t xnvme_timer_stop(xnvme_timer* t)

    double xnvme_timer_elapsed_secs(xnvme_timer* t)

    double xnvme_timer_elapsed(xnvme_timer* t)

    double xnvme_timer_elapsed_msecs(xnvme_timer* t)

    double xnvme_timer_elapsed_usecs(xnvme_timer* t)

    uint64_t xnvme_timer_elapsed_nsecs(xnvme_timer* t)

    void xnvme_timer_pr(xnvme_timer* t, char* prefix)

    void xnvme_timer_bw_pr(xnvme_timer* t, char* prefix, size_t nbytes)

    int xnvme_is_pow2(uint32_t val)

    cpdef enum xnvme_geo_type:
        XNVME_GEO_UNKNOWN
        XNVME_GEO_CONVENTIONAL
        XNVME_GEO_ZONED

    cdef struct xnvme_geo:
        xnvme_geo_type type
        uint32_t npugrp
        uint32_t npunit
        uint32_t nzone
        uint64_t nsect
        uint32_t nbytes
        uint32_t nbytes_oob
        uint64_t tbytes
        uint64_t ssw
        uint32_t mdts_nbytes
        uint32_t lba_nbytes
        uint8_t lba_extended
        uint8_t _rsvd[7]

    cdef struct xnvme_ident:
        char uri[384]
        uint32_t dtype
        uint32_t nsid
        uint8_t csi
        uint8_t rsvd[3]

    int xnvme_ident_from_uri(char* uri, xnvme_ident* ident)

    cdef struct xnvme_spec_ctrlr_bar:
        uint64_t cap
        uint32_t vs
        uint32_t intms
        uint32_t intmc
        uint32_t cc
        uint32_t rsvd24
        uint32_t csts
        uint32_t nssr
        uint32_t aqa
        uint64_t asq
        uint64_t acq
        uint32_t cmbloc
        uint32_t cmbsz
        uint32_t bpinfo
        uint32_t bprsel
        uint64_t bpmbl
        uint64_t cmbmsc
        uint32_t cmbsts
        uint8_t rsvd92[3492]
        uint32_t pmrcap
        uint32_t pmrctl
        uint32_t pmrsts
        uint32_t pmrebs
        uint32_t pmrswtp
        uint32_t pmrmscl
        uint32_t pmrmscu
        uint8_t css[484]

    cpdef enum xnvme_spec_status_code_type:
        XNVME_STATUS_CODE_TYPE_GENERIC
        XNVME_STATUS_CODE_TYPE_CMDSPEC
        XNVME_STATUS_CODE_TYPE_MEDIA
        XNVME_STATUS_CODE_TYPE_PATH
        XNVME_STATUS_CODE_TYPE_VENDOR

    cdef struct xnvme_spec_status:
        uint16_t val
        uint16_t p
        uint16_t sc
        uint16_t sct
        uint16_t rsvd2
        uint16_t m
        uint16_t dnr

    cdef struct xnvme_spec_cpl:
        uint16_t sqhd
        uint16_t sqid
        uint16_t cid
        xnvme_spec_status status
        uint64_t result
        uint32_t cdw0
        uint32_t rsvd1

    cdef struct xnvme_spec_log_health_entry:
        uint8_t crit_warn
        uint16_t comp_temp
        uint8_t avail_spare
        uint8_t avail_spare_thresh
        uint8_t pct_used
        uint8_t eg_crit_warn_sum
        uint8_t rsvd8[25]
        uint8_t data_units_read[16]
        uint8_t data_units_written[16]
        uint8_t host_read_cmds[16]
        uint8_t host_write_cmds[16]
        uint8_t ctrlr_busy_time[16]
        uint8_t pwr_cycles[16]
        uint8_t pwr_on_hours[16]
        uint8_t unsafe_shutdowns[16]
        uint8_t mdi_errs[16]
        uint8_t nr_err_logs[16]
        uint32_t warn_comp_temp_time
        uint32_t crit_comp_temp_time
        uint16_t temp_sens[8]
        uint32_t tmt1tc
        uint32_t tmt2tc
        uint32_t tttmt1
        uint32_t tttmt2
        uint8_t rsvd[280]

    cdef struct xnvme_spec_log_erri_entry:
        uint64_t ecnt
        uint16_t sqid
        uint16_t cid
        xnvme_spec_status status
        uint16_t eloc
        uint64_t lba
        uint32_t nsid
        uint8_t ven_si
        uint8_t trtype
        uint8_t reserved30[2]
        uint64_t cmd_si
        uint16_t trtype_si
        uint8_t reserved42[22]

    cpdef enum xnvme_spec_log_lpi:
        XNVME_SPEC_LOG_RSVD
        XNVME_SPEC_LOG_ERRI
        XNVME_SPEC_LOG_HEALTH
        XNVME_SPEC_LOG_FW
        XNVME_SPEC_LOG_CHNS
        XNVME_SPEC_LOG_CSAE
        XNVME_SPEC_LOG_SELFTEST
        XNVME_SPEC_LOG_TELEHOST
        XNVME_SPEC_LOG_TELECTRLR

    cpdef enum xnvme_spec_idfy_cns:
        XNVME_SPEC_IDFY_NS
        XNVME_SPEC_IDFY_CTRLR
        XNVME_SPEC_IDFY_NSLIST
        XNVME_SPEC_IDFY_NSDSCR
        XNVME_SPEC_IDFY_SETL
        XNVME_SPEC_IDFY_NS_IOCS
        XNVME_SPEC_IDFY_CTRLR_IOCS
        XNVME_SPEC_IDFY_NSLIST_IOCS
        XNVME_SPEC_IDFY_NSLIST_ALLOC
        XNVME_SPEC_IDFY_NS_ALLOC
        XNVME_SPEC_IDFY_CTRLR_NS
        XNVME_SPEC_IDFY_CTRLR_SUB
        XNVME_SPEC_IDFY_CTRLR_PRI
        XNVME_SPEC_IDFY_CTRLR_SEC
        XNVME_SPEC_IDFY_NSGRAN
        XNVME_SPEC_IDFY_UUIDL
        XNVME_SPEC_IDFY_NSLIST_ALLOC_IOCS
        XNVME_SPEC_IDFY_NS_ALLOC_IOCS
        XNVME_SPEC_IDFY_IOCS

    cdef struct xnvme_spec_lbaf:
        uint16_t ms
        uint8_t ds
        uint8_t rp
        uint8_t rsvd

    cpdef enum xnvme_spec_csi:
        XNVME_SPEC_CSI_NVM
        XNVME_SPEC_CSI_ZONED

    cdef struct xnvme_spec_idfy_ns:
        uint64_t nsze
        uint64_t ncap
        uint64_t nuse
        uint8_t nlbaf
        uint16_t nawun
        uint16_t nawupf
        uint16_t nacwu
        uint16_t nabsn
        uint16_t nabo
        uint16_t nabspf
        uint16_t noiob
        uint64_t nvmcap[2]
        uint8_t reserved64[40]
        uint8_t nguid[16]
        uint64_t eui64
        xnvme_spec_lbaf lbaf[16]
        uint8_t rsvd3776[3648]
        uint8_t vendor_specific[256]
        uint8_t nsfeat__thin_prov "nsfeat.thin_prov"
        uint8_t nsfeat__ns_atomic_write_unit "nsfeat.ns_atomic_write_unit"
        uint8_t nsfeat__dealloc_or_unwritten_error "nsfeat.dealloc_or_unwritten_error"
        uint8_t nsfeat__guid_never_reused "nsfeat.guid_never_reused"
        uint8_t nsfeat__reserved1 "nsfeat.reserved1"
        uint8_t flbas__format "flbas.format"
        uint8_t flbas__extended "flbas.extended"
        uint8_t flbas__reserved2 "flbas.reserved2"
        uint8_t mc__extended "mc.extended"
        uint8_t mc__pointer "mc.pointer"
        uint8_t mc__reserved3 "mc.reserved3"
        uint8_t dpc__val "dpc.val"
        uint8_t dpc__pit1 "dpc.pit1"
        uint8_t dpc__pit2 "dpc.pit2"
        uint8_t dpc__pit3 "dpc.pit3"
        uint8_t dpc__md_start "dpc.md_start"
        uint8_t dpc__md_end "dpc.md_end"
        uint8_t dps__val "dps.val"
        uint8_t dps__pit "dps.pit"
        uint8_t dps__md_start "dps.md_start"
        uint8_t dps__reserved4 "dps.reserved4"
        uint8_t nmic__can_share "nmic.can_share"
        uint8_t nmic__reserved "nmic.reserved"
        uint8_t nsrescap__val "nsrescap.val"
        uint8_t nsrescap__persist "nsrescap.persist"
        uint8_t nsrescap__write_exclusive "nsrescap.write_exclusive"
        uint8_t nsrescap__exclusive_access "nsrescap.exclusive_access"
        uint8_t nsrescap__write_exclusive_reg_only "nsrescap.write_exclusive_reg_only"
        uint8_t nsrescap__exclusive_access_reg_only "nsrescap.exclusive_access_reg_only"
        uint8_t nsrescap__write_exclusive_all_reg "nsrescap.write_exclusive_all_reg"
        uint8_t nsrescap__exclusive_access_all_reg "nsrescap.exclusive_access_all_reg"
        uint8_t nsrescap__ignore_existing_key "nsrescap.ignore_existing_key"
        uint8_t fpi__val "fpi.val"
        uint8_t fpi__percentage_remaining "fpi.percentage_remaining"
        uint8_t fpi__fpi_supported "fpi.fpi_supported"
        uint8_t dlfeat__val "dlfeat.val"
        uint8_t dlfeat__bits__read_value "dlfeat.bits.read_value"
        uint8_t dlfeat__bits__write_zero_deallocate "dlfeat.bits.write_zero_deallocate"
        uint8_t dlfeat__bits__guard_value "dlfeat.bits.guard_value"
        uint8_t dlfeat__bits__reserved "dlfeat.bits.reserved"

    cdef struct xnvme_spec_power_state:
        uint16_t mp
        uint8_t reserved1
        uint8_t mps
        uint8_t nops
        uint8_t reserved2
        uint32_t enlat
        uint32_t exlat
        uint8_t rrt
        uint8_t reserved3
        uint8_t rrl
        uint8_t reserved4
        uint8_t rwt
        uint8_t reserved5
        uint8_t rwl
        uint8_t reserved6
        uint8_t reserved7[16]

    cdef union xnvme_spec_vs_register:
        uint32_t val
        uint32_t bits__ter "bits.ter"
        uint32_t bits__mnr "bits.mnr"
        uint32_t bits__mjr "bits.mjr"

    cdef struct xnvme_spec_idfy_ctrlr:
        uint16_t vid
        uint16_t ssvid
        int8_t sn[20]
        int8_t mn[40]
        uint8_t fr[8]
        uint8_t rab
        uint8_t ieee[3]
        uint8_t mdts
        uint16_t cntlid
        xnvme_spec_vs_register ver
        uint32_t rtd3r
        uint32_t rtd3e
        uint8_t reserved_100[12]
        uint8_t fguid[16]
        uint8_t reserved_128[128]
        uint8_t acl
        uint8_t aerl
        uint8_t elpe
        uint8_t npss
        uint16_t wctemp
        uint16_t cctemp
        uint16_t mtfa
        uint32_t hmpre
        uint32_t hmmin
        uint64_t tnvmcap[2]
        uint64_t unvmcap[2]
        uint16_t edstt
        uint8_t fwug
        uint16_t kas
        uint16_t mntmt
        uint16_t mxtmt
        uint8_t reserved3[180]
        uint16_t maxcmd
        uint32_t nn
        uint16_t fuses
        uint16_t awun
        uint16_t awupf
        uint8_t nvscc
        uint8_t reserved531
        uint16_t acwu
        uint16_t reserved534
        uint32_t mnan
        uint8_t reserved4[224]
        uint8_t subnqn[256]
        uint8_t reserved5[768]
        xnvme_spec_power_state psd[32]
        uint8_t vs[1024]
        uint8_t cmic__val "cmic.val"
        uint8_t cmic__multi_port "cmic.multi_port"
        uint8_t cmic__multi_host "cmic.multi_host"
        uint8_t cmic__sr_iov "cmic.sr_iov"
        uint8_t cmic__reserved "cmic.reserved"
        uint32_t oaes__val "oaes.val"
        uint32_t oaes__reserved1 "oaes.reserved1"
        uint32_t oaes__ns_attribute_notices "oaes.ns_attribute_notices"
        uint32_t oaes__fw_activation_notices "oaes.fw_activation_notices"
        uint32_t oaes__reserved2 "oaes.reserved2"
        uint32_t oaes__zone_changes "oaes.zone_changes"
        uint32_t oaes__reserved3 "oaes.reserved3"
        uint32_t ctratt__val "ctratt.val"
        uint32_t ctratt__host_id_exhid_supported "ctratt.host_id_exhid_supported"
        uint32_t ctratt__non_operational_power_state_permissive_mode "ctratt.non_operational_power_state_permissive_mode"
        uint32_t ctratt__reserved "ctratt.reserved"
        uint16_t oacs__val "oacs.val"
        uint16_t oacs__security "oacs.security"
        uint16_t oacs__format "oacs.format"
        uint16_t oacs__firmware "oacs.firmware"
        uint16_t oacs__ns_manage "oacs.ns_manage"
        uint16_t oacs__device_self_test "oacs.device_self_test"
        uint16_t oacs__directives "oacs.directives"
        uint16_t oacs__nvme_mi "oacs.nvme_mi"
        uint16_t oacs__virtualization_management "oacs.virtualization_management"
        uint16_t oacs__doorbell_buffer_config "oacs.doorbell_buffer_config"
        uint16_t oacs__oacs_rsvd "oacs.oacs_rsvd"
        uint8_t frmw__val "frmw.val"
        uint8_t frmw__slot1_ro "frmw.slot1_ro"
        uint8_t frmw__num_slots "frmw.num_slots"
        uint8_t frmw__activation_without_reset "frmw.activation_without_reset"
        uint8_t frmw__frmw_rsvd "frmw.frmw_rsvd"
        uint8_t lpa__val "lpa.val"
        uint8_t lpa__ns_smart "lpa.ns_smart"
        uint8_t lpa__celp "lpa.celp"
        uint8_t lpa__edlp "lpa.edlp"
        uint8_t lpa__telemetry "lpa.telemetry"
        uint8_t lpa__pel "lpa.pel"
        uint8_t lpa__lpa_rsvd "lpa.lpa_rsvd"
        uint8_t avscc__val "avscc.val"
        uint8_t avscc__spec_format "avscc.spec_format"
        uint8_t avscc__avscc_rsvd "avscc.avscc_rsvd"
        uint8_t apsta__val "apsta.val"
        uint8_t apsta__supported "apsta.supported"
        uint8_t apsta__apsta_rsvd "apsta.apsta_rsvd"
        uint32_t rpmbs__val "rpmbs.val"
        uint8_t rpmbs__num_rpmb_units "rpmbs.num_rpmb_units"
        uint8_t rpmbs__auth_method "rpmbs.auth_method"
        uint8_t rpmbs__reserved1 "rpmbs.reserved1"
        uint8_t rpmbs__reserved2 "rpmbs.reserved2"
        uint8_t rpmbs__total_size "rpmbs.total_size"
        uint8_t rpmbs__access_size "rpmbs.access_size"
        uint8_t dsto__val "dsto.val"
        uint8_t dsto__bits__one_only "dsto.bits.one_only"
        uint8_t dsto__bits__reserved "dsto.bits.reserved"
        uint16_t hctma__val "hctma.val"
        uint16_t hctma__bits__supported "hctma.bits.supported"
        uint16_t hctma__bits__reserved "hctma.bits.reserved"
        uint32_t sanicap__val "sanicap.val"
        uint32_t sanicap__bits__crypto_erase "sanicap.bits.crypto_erase"
        uint32_t sanicap__bits__block_erase "sanicap.bits.block_erase"
        uint32_t sanicap__bits__overwrite "sanicap.bits.overwrite"
        uint32_t sanicap__bits__reserved "sanicap.bits.reserved"
        uint8_t sqes__val "sqes.val"
        uint8_t sqes__min "sqes.min"
        uint8_t sqes__max "sqes.max"
        uint8_t cqes__val "cqes.val"
        uint8_t cqes__min "cqes.min"
        uint8_t cqes__max "cqes.max"
        uint16_t oncs__val "oncs.val"
        uint16_t oncs__compare "oncs.compare"
        uint16_t oncs__write_unc "oncs.write_unc"
        uint16_t oncs__dsm "oncs.dsm"
        uint16_t oncs__write_zeroes "oncs.write_zeroes"
        uint16_t oncs__set_features_save "oncs.set_features_save"
        uint16_t oncs__reservations "oncs.reservations"
        uint16_t oncs__timestamp "oncs.timestamp"
        uint16_t oncs__reserved "oncs.reserved"
        uint8_t fna__val "fna.val"
        uint8_t fna__format_all_ns "fna.format_all_ns"
        uint8_t fna__erase_all_ns "fna.erase_all_ns"
        uint8_t fna__crypto_erase_supported "fna.crypto_erase_supported"
        uint8_t fna__reserved "fna.reserved"
        uint8_t vwc__val "vwc.val"
        uint8_t vwc__present "vwc.present"
        uint8_t vwc__flush_broadcast "vwc.flush_broadcast"
        uint8_t vwc__reserved "vwc.reserved"
        uint32_t sgls__val "sgls.val"
        uint32_t sgls__supported "sgls.supported"
        uint32_t sgls__keyed_sgl "sgls.keyed_sgl"
        uint32_t sgls__reserved1 "sgls.reserved1"
        uint32_t sgls__bit_bucket_descriptor "sgls.bit_bucket_descriptor"
        uint32_t sgls__metadata_pointer "sgls.metadata_pointer"
        uint32_t sgls__oversized_sgl "sgls.oversized_sgl"
        uint32_t sgls__metadata_address "sgls.metadata_address"
        uint32_t sgls__sgl_offset "sgls.sgl_offset"
        uint32_t sgls__transport_sgl "sgls.transport_sgl"
        uint32_t sgls__reserved2 "sgls.reserved2"
        uint32_t nvmf_specific__ioccsz "nvmf_specific.ioccsz"
        uint32_t nvmf_specific__iorcsz "nvmf_specific.iorcsz"
        uint16_t nvmf_specific__icdoff "nvmf_specific.icdoff"
        uint8_t nvmf_specific__msdbd "nvmf_specific.msdbd"
        uint8_t nvmf_specific__reserved "nvmf_specific.reserved[244]"
        uint8_t nvmf_specific__ctrattr__ctrlr_model "nvmf_specific.ctrattr.ctrlr_model"
        uint8_t nvmf_specific__ctrattr__reserved "nvmf_specific.ctrattr.reserved"

    cdef struct xnvme_spec_cs_vector:
        uint64_t val
        uint64_t nvm
        uint64_t rsvd1
        uint64_t zns
        uint64_t rsvd

    cdef struct xnvme_spec_idfy_cs:
        xnvme_spec_cs_vector iocsc[512]

    cdef struct xnvme_spec_idfy:
        xnvme_spec_idfy_ctrlr ctrlr
        xnvme_spec_idfy_ns ns
        xnvme_spec_idfy_cs cs

    cpdef enum xnvme_spec_adm_opc:
        XNVME_SPEC_ADM_OPC_LOG
        XNVME_SPEC_ADM_OPC_IDFY
        XNVME_SPEC_ADM_OPC_SFEAT
        XNVME_SPEC_ADM_OPC_GFEAT

    cpdef enum xnvme_spec_nvm_opc:
        XNVME_SPEC_NVM_OPC_FLUSH
        XNVME_SPEC_NVM_OPC_WRITE
        XNVME_SPEC_NVM_OPC_READ
        XNVME_SPEC_NVM_OPC_WRITE_UNCORRECTABLE
        XNVME_SPEC_NVM_OPC_WRITE_ZEROES
        XNVME_SPEC_NVM_OPC_SCOPY
        XNVME_SPEC_NVM_OPC_FMT
        XNVME_SPEC_NVM_OPC_SANITIZE

    cpdef enum xnvme_spec_feat_id:
        XNVME_SPEC_FEAT_ARBITRATION
        XNVME_SPEC_FEAT_PWR_MGMT
        XNVME_SPEC_FEAT_LBA_RANGETYPE
        XNVME_SPEC_FEAT_TEMP_THRESHOLD
        XNVME_SPEC_FEAT_ERROR_RECOVERY
        XNVME_SPEC_FEAT_VWCACHE
        XNVME_SPEC_FEAT_NQUEUES

    cpdef enum xnvme_spec_feat_sel:
        XNVME_SPEC_FEAT_SEL_CURRENT
        XNVME_SPEC_FEAT_SEL_DEFAULT
        XNVME_SPEC_FEAT_SEL_SAVED
        XNVME_SPEC_FEAT_SEL_SUPPORTED

    cdef struct xnvme_spec_feat:
        uint32_t val
        uint32_t temp_threshold__tmpth "temp_threshold.tmpth"
        uint32_t temp_threshold__tmpsel "temp_threshold.tmpsel"
        uint32_t temp_threshold__thsel "temp_threshold.thsel"
        uint32_t error_recovery__tler "error_recovery.tler"
        uint32_t error_recovery__dulbe "error_recovery.dulbe"
        uint32_t error_recovery__rsvd "error_recovery.rsvd"
        uint32_t nqueues__nsqa "nqueues.nsqa"
        uint32_t nqueues__ncqa "nqueues.ncqa"

    cdef struct xnvme_spec_dsm_range:
        uint32_t cattr
        uint32_t nlb
        uint64_t slba

    cpdef enum xnvme_spec_flag:
        XNVME_SPEC_FLAG_LIMITED_RETRY
        XNVME_SPEC_FLAG_FORCE_UNIT_ACCESS
        XNVME_SPEC_FLAG_PRINFO_PRCHK_REF
        XNVME_SPEC_FLAG_PRINFO_PRCHK_APP
        XNVME_SPEC_FLAG_PRINFO_PRCHK_GUARD
        XNVME_SPEC_FLAG_PRINFO_PRACT

    cpdef enum xnvme_nvme_sgl_descriptor_type:
        XNVME_SPEC_SGL_DESCR_TYPE_DATA_BLOCK
        XNVME_SPEC_SGL_DESCR_TYPE_BIT_BUCKET
        XNVME_SPEC_SGL_DESCR_TYPE_SEGMENT
        XNVME_SPEC_SGL_DESCR_TYPE_LAST_SEGMENT
        XNVME_SPEC_SGL_DESCR_TYPE_KEYED_DATA_BLOCK
        XNVME_SPEC_SGL_DESCR_TYPE_VENDOR_SPECIFIC

    cpdef enum xnvme_spec_sgl_descriptor_subtype:
        XNVME_SPEC_SGL_DESCR_SUBTYPE_ADDRESS
        XNVME_SPEC_SGL_DESCR_SUBTYPE_OFFSET

    cdef struct xnvme_spec_sgl_descriptor:
        uint64_t addr
        uint64_t generic__rsvd "generic.rsvd"
        uint64_t generic__subtype "generic.subtype"
        uint64_t generic__type "generic.type"
        uint64_t unkeyed__len "unkeyed.len"
        uint64_t unkeyed__rsvd "unkeyed.rsvd"
        uint64_t unkeyed__subtype "unkeyed.subtype"
        uint64_t unkeyed__type "unkeyed.type"

    cpdef enum xnvme_spec_psdt:
        XNVME_SPEC_PSDT_PRP
        XNVME_SPEC_PSDT_SGL_MPTR_CONTIGUOUS
        XNVME_SPEC_PSDT_SGL_MPTR_SGL

    cdef struct xnvme_spec_cmd_common:
        uint16_t opcode
        uint16_t fuse
        uint16_t rsvd
        uint16_t psdt
        uint16_t cid
        uint32_t nsid
        uint32_t cdw02
        uint32_t cdw03
        uint64_t mptr
        uint32_t ndt
        uint32_t ndm
        uint32_t cdw12
        uint32_t cdw13
        uint32_t cdw14
        uint32_t cdw15
        xnvme_spec_sgl_descriptor dptr__sgl "dptr.sgl"
        uint64_t dptr__prp__prp1 "dptr.prp.prp1"
        uint64_t dptr__prp__prp2 "dptr.prp.prp2"
        uint64_t dptr__lnx_ioctl__data "dptr.lnx_ioctl.data"
        uint32_t dptr__lnx_ioctl__metadata_len "dptr.lnx_ioctl.metadata_len"
        uint32_t dptr__lnx_ioctl__data_len "dptr.lnx_ioctl.data_len"

    cdef struct xnvme_spec_cmd_sanitize:
        uint32_t cdw00_09[10]
        uint32_t sanact
        uint32_t ause
        uint32_t owpass
        uint32_t oipbp
        uint32_t nodas
        uint32_t rsvd
        uint32_t ovrpat
        uint32_t cdw12_15[4]

    cdef struct xnvme_spec_cmd_format:
        uint32_t cdw00_09[10]
        uint32_t lbaf
        uint32_t mset
        uint32_t pi
        uint32_t pil
        uint32_t ses
        uint32_t zf
        uint32_t rsvd
        uint32_t cdw11_15[5]

    cdef struct xnvme_spec_cmd_gfeat:
        uint32_t cdw00_09[10]
        uint32_t cdw11_15[5]
        uint32_t cdw10__val "cdw10.val"
        uint32_t cdw10__fid "cdw10.fid"
        uint32_t cdw10__sel "cdw10.sel"
        uint32_t cdw10__rsvd10 "cdw10.rsvd10"

    cdef struct xnvme_spec_cmd_sfeat:
        uint32_t cdw00_09[10]
        xnvme_spec_feat feat
        uint32_t cdw12_15[4]
        uint32_t cdw10__val "cdw10.val"
        uint32_t cdw10__fid "cdw10.fid"
        uint32_t cdw10__rsvd10 "cdw10.rsvd10"
        uint32_t cdw10__save "cdw10.save"

    cdef struct xnvme_spec_cmd_idfy:
        uint32_t cdw00_09[10]
        uint32_t cns
        uint32_t rsvd1
        uint32_t cntid
        uint32_t nvmsetid
        uint32_t rsvd2
        uint32_t csi
        uint32_t cdw12_13[2]
        uint32_t uuid
        uint32_t rsvd3
        uint32_t cdw15

    cdef struct xnvme_spec_cmd_log:
        uint32_t cdw00_09[10]
        uint32_t lid
        uint32_t lsp
        uint32_t rsvd10
        uint32_t rae
        uint32_t numdl
        uint32_t numdu
        uint32_t rsvd11
        uint32_t lpol
        uint32_t lpou
        uint32_t cdw14_15[2]

    cdef struct xnvme_spec_cmd_nvm:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd
        uint32_t dtype
        uint32_t rsvd2
        uint32_t prinfo
        uint32_t fua
        uint32_t lr
        uint32_t cdw13_15[3]

    cdef struct xnvme_spec_nvm_write_zeroes:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd1
        uint32_t deac
        uint32_t prinfo
        uint32_t fua
        uint32_t lr
        uint32_t cdw_13
        uint32_t ilbrt
        uint32_t lbat
        uint32_t lbatm

    cpdef enum xnvme_spec_nvm_cmd_cpl_sc:
        XNVME_SPEC_NVM_CMD_CPL_SC_WRITE_TO_RONLY

    cdef struct xnvme_spec_nvm_scopy_fmt_zero:
        uint8_t rsvd0[8]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd20
        uint32_t eilbrt
        uint32_t elbatm
        uint32_t elbat

    cpdef enum xnvme_nvm_scopy_fmt:
        XNVME_NVM_SCOPY_FMT_ZERO
        XNVME_NVM_SCOPY_FMT_SRCLEN

    cdef struct xnvme_spec_nvm_scopy_source_range:
        xnvme_spec_nvm_scopy_fmt_zero entry[128]

    cdef struct xnvme_spec_nvm_cmd_scopy:
        uint32_t cdw00_09[10]
        uint64_t sdlba
        uint32_t nr
        uint32_t df
        uint32_t prinfor
        uint32_t rsvd1
        uint32_t dtype
        uint32_t rsvd2
        uint32_t prinfow
        uint32_t fua
        uint32_t lr
        uint32_t rsvd3
        uint32_t dspec
        uint32_t ilbrt
        uint32_t lbat
        uint32_t lbatm

    cdef struct xnvme_spec_nvm_cmd_scopy_fmt_srclen:
        uint64_t start
        uint64_t len

    cdef struct xnvme_spec_nvm_cmd:
        xnvme_spec_nvm_cmd_scopy scopy

    cdef struct xnvme_spec_nvm_idfy_ctrlr:
        uint8_t byte0_519[520]
        uint8_t byte522_533[12]
        uint8_t byte536_4095[3559]
        uint16_t oncs__val "oncs.val"
        uint16_t oncs__compare "oncs.compare"
        uint16_t oncs__write_unc "oncs.write_unc"
        uint16_t oncs__dsm "oncs.dsm"
        uint16_t oncs__write_zeroes "oncs.write_zeroes"
        uint16_t oncs__set_features_save "oncs.set_features_save"
        uint16_t oncs__reservations "oncs.reservations"
        uint16_t oncs__timestamp "oncs.timestamp"
        uint16_t oncs__verify "oncs.verify"
        uint16_t oncs__copy "oncs.copy"
        uint16_t oncs__reserved "oncs.reserved"
        uint16_t ocfs__val "ocfs.val"
        uint16_t ocfs__copy_fmt0 "ocfs.copy_fmt0"
        uint16_t ocfs__rsvd "ocfs.rsvd"

    cdef struct xnvme_spec_nvm_idfy_ns:
        uint8_t byte0_73[74]
        uint16_t mssrl
        uint32_t mcl
        uint8_t msrc
        uint8_t byte81_4095[4014]

    cdef struct xnvme_spec_nvm_idfy:
        xnvme_spec_idfy base
        xnvme_spec_nvm_idfy_ctrlr ctrlr
        xnvme_spec_nvm_idfy_ns ns

    cpdef enum xnvme_spec_znd_log_lid:
        XNVME_SPEC_LOG_ZND_CHANGES

    cpdef enum xnvme_spec_znd_opc:
        XNVME_SPEC_ZND_OPC_MGMT_SEND
        XNVME_SPEC_ZND_OPC_MGMT_RECV
        XNVME_SPEC_ZND_OPC_APPEND

    cdef struct xnvme_spec_znd_cmd_mgmt_send:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nrange
        uint32_t zsa
        uint32_t select_all
        uint32_t zsaso
        uint32_t rsvd
        uint32_t cdw14_15[2]

    cdef struct xnvme_spec_znd_cmd_mgmt_recv:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t ndwords
        uint32_t zra
        uint32_t zrasf
        uint32_t partial
        uint32_t rsvd
        uint64_t addrs_dst

    cdef struct xnvme_spec_znd_cmd_append:
        uint32_t cdw00_09[10]
        uint64_t zslba
        uint32_t nlb
        uint32_t rsvd
        uint32_t dtype
        uint32_t prinfo
        uint32_t rsvd2
        uint32_t fua
        uint32_t lr
        uint32_t cdw13_15[3]

    cdef struct xnvme_spec_znd_cmd:
        xnvme_spec_znd_cmd_mgmt_send mgmt_send
        xnvme_spec_znd_cmd_mgmt_recv mgmt_recv
        xnvme_spec_znd_cmd_append append

    cdef struct xnvme_spec_cmd:
        xnvme_spec_cmd_common common
        xnvme_spec_cmd_sanitize sanitize
        xnvme_spec_cmd_format format
        xnvme_spec_cmd_log log
        xnvme_spec_cmd_gfeat gfeat
        xnvme_spec_cmd_sfeat sfeat
        xnvme_spec_cmd_idfy idfy
        xnvme_spec_cmd_nvm nvm
        xnvme_spec_nvm_cmd_scopy scopy
        xnvme_spec_nvm_write_zeroes write_zeroes
        xnvme_spec_znd_cmd znd

    cpdef enum xnvme_spec_znd_status_code:
        XNVME_SPEC_ZND_SC_INVALID_FORMAT
        XNVME_SPEC_ZND_SC_INVALID_ZONE_OP
        XNVME_SPEC_ZND_SC_NOZRWA
        XNVME_SPEC_ZND_SC_BOUNDARY_ERROR
        XNVME_SPEC_ZND_SC_IS_FULL
        XNVME_SPEC_ZND_SC_IS_READONLY
        XNVME_SPEC_ZND_SC_IS_OFFLINE
        XNVME_SPEC_ZND_SC_INVALID_WRITE
        XNVME_SPEC_ZND_SC_TOO_MANY_ACTIVE
        XNVME_SPEC_ZND_SC_TOO_MANY_OPEN
        XNVME_SPEC_ZND_SC_INVALID_TRANS

    cpdef enum xnvme_spec_znd_mgmt_send_action_so:
        XNVME_SPEC_ZND_MGMT_OPEN_WITH_ZRWA

    cpdef enum xnvme_spec_znd_cmd_mgmt_send_action:
        XNVME_SPEC_ZND_CMD_MGMT_SEND_CLOSE
        XNVME_SPEC_ZND_CMD_MGMT_SEND_FINISH
        XNVME_SPEC_ZND_CMD_MGMT_SEND_OPEN
        XNVME_SPEC_ZND_CMD_MGMT_SEND_RESET
        XNVME_SPEC_ZND_CMD_MGMT_SEND_OFFLINE
        XNVME_SPEC_ZND_CMD_MGMT_SEND_DESCRIPTOR
        XNVME_SPEC_ZND_CMD_MGMT_SEND_FLUSH

    cpdef enum xnvme_spec_znd_cmd_mgmt_recv_action_sf:
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_ALL
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_EMPTY
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_IOPEN
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_EOPEN
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_CLOSED
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_FULL
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_RONLY
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_OFFLINE

    cpdef enum xnvme_spec_znd_cmd_mgmt_recv_action:
        XNVME_SPEC_ZND_CMD_MGMT_RECV_ACTION_REPORT
        XNVME_SPEC_ZND_CMD_MGMT_RECV_ACTION_REPORT_EXTENDED

    cpdef enum xnvme_spec_znd_type:
        XNVME_SPEC_ZND_TYPE_SEQWR

    cpdef enum xnvme_spec_znd_state:
        XNVME_SPEC_ZND_STATE_EMPTY
        XNVME_SPEC_ZND_STATE_IOPEN
        XNVME_SPEC_ZND_STATE_EOPEN
        XNVME_SPEC_ZND_STATE_CLOSED
        XNVME_SPEC_ZND_STATE_RONLY
        XNVME_SPEC_ZND_STATE_FULL
        XNVME_SPEC_ZND_STATE_OFFLINE

    cdef struct xnvme_spec_znd_idfy_ctrlr:
        uint8_t zasl
        uint8_t rsvd8[4095]

    cdef struct xnvme_spec_znd_idfy_lbafe:
        uint64_t zsze
        uint8_t zdes
        uint8_t rsvd[7]

    cdef struct xnvme_spec_znd_idfy_ns:
        uint32_t mar
        uint32_t mor
        uint32_t rrl
        uint32_t frl
        uint8_t rsvd12[24]
        uint32_t numzrwa
        uint16_t zrwafg
        uint16_t zrwas
        uint8_t rsvd53[2763]
        xnvme_spec_znd_idfy_lbafe lbafe[16]
        uint8_t rsvd3072[768]
        uint8_t vs[256]
        uint16_t zoc__val "zoc.val"
        uint16_t zoc__bits__vzcap "zoc.bits.vzcap"
        uint16_t zoc__bits__zae "zoc.bits.zae"
        uint16_t zoc__bits__rsvd "zoc.bits.rsvd"
        uint16_t ozcs__val "ozcs.val"
        uint16_t ozcs__bits__razb "ozcs.bits.razb"
        uint16_t ozcs__bits__zrwasup "ozcs.bits.zrwasup"
        uint16_t ozcs__bits__rsvd "ozcs.bits.rsvd"
        uint8_t zrwacap__val "zrwacap.val"
        uint8_t zrwacap__bits__expflushsup "zrwacap.bits.expflushsup"
        uint8_t zrwacap__bits__rsvd0 "zrwacap.bits.rsvd0"

    cdef struct xnvme_spec_znd_idfy:
        xnvme_spec_idfy base
        xnvme_spec_znd_idfy_ctrlr zctrlr
        xnvme_spec_znd_idfy_ns zns

    cdef struct xnvme_spec_znd_log_changes:
        uint16_t nidents
        uint8_t rsvd2[6]
        uint64_t idents[511]

    cdef struct xnvme_spec_znd_descr:
        uint8_t zt
        uint8_t rsvd0
        uint8_t rsvd1
        uint8_t zs
        uint8_t rsvd7[5]
        uint64_t zcap
        uint64_t zslba
        uint64_t wp
        uint8_t rsvd63[32]
        uint8_t za__val "za.val"
        uint8_t za__zfc "za.zfc"
        uint8_t za__zfr "za.zfr"
        uint8_t za__rzr "za.rzr"
        uint8_t za__zrwav "za.zrwav"
        uint8_t za__rsvd3 "za.rsvd3"
        uint8_t za__zdev "za.zdev"

    cdef struct xnvme_spec_znd_report_hdr:
        uint64_t nzones
        uint8_t rsvd[56]

    int xnvme_spec_log_health_fpr(void* stream, xnvme_spec_log_health_entry* log, int opts)

    int xnvme_spec_log_health_pr(xnvme_spec_log_health_entry* log, int opts)

    int xnvme_spec_log_erri_fpr(void* stream, xnvme_spec_log_erri_entry* log, int limit, int opts)

    int xnvme_spec_log_erri_pr(xnvme_spec_log_erri_entry* log, int limit, int opts)

    int xnvme_spec_idfy_ns_fpr(void* stream, xnvme_spec_idfy_ns* idfy, int opts)

    int xnvme_spec_idfy_ns_pr(xnvme_spec_idfy_ns* idfy, int opts)

    int xnvme_spec_idfy_ctrl_fpr(void* stream, xnvme_spec_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_idfy_ctrl_pr(xnvme_spec_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_idfy_cs_fpr(void* stream, xnvme_spec_idfy_cs* idfy, int opts)

    int xnvme_spec_idfy_cs_pr(xnvme_spec_idfy_cs* idfy, int opts)

    int xnvme_spec_feat_fpr(void* stream, uint8_t fid, xnvme_spec_feat feat, int opts)

    int xnvme_spec_feat_pr(uint8_t fid, xnvme_spec_feat feat, int opts)

    int xnvme_spec_cmd_fpr(void* stream, xnvme_spec_cmd* cmd, int opts)

    int xnvme_spec_cmd_pr(xnvme_spec_cmd* cmd, int opts)

    int xnvme_spec_nvm_scopy_fmt_zero_fpr(void* stream, xnvme_spec_nvm_scopy_fmt_zero* entry, int opts)

    int xnvme_spec_nvm_scopy_fmt_zero_pr(xnvme_spec_nvm_scopy_fmt_zero* entry, int opts)

    int xnvme_spec_nvm_scopy_source_range_fpr(void* stream, xnvme_spec_nvm_scopy_source_range* srange, uint8_t nr, int opts)

    int xnvme_spec_nvm_scopy_source_range_pr(xnvme_spec_nvm_scopy_source_range* srange, uint8_t nr, int opts)

    int xnvme_spec_idfy_ctrlr_fpr(void* stream, xnvme_spec_nvm_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_nvm_idfy_ctrlr_pr(xnvme_spec_nvm_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_nvm_idfy_ns_fpr(void* stream, xnvme_spec_nvm_idfy_ns* idfy, int opts)

    int xnvme_spec_nvm_idfy_ns_pr(xnvme_spec_nvm_idfy_ns* idfy, int opts)

    int xnvme_spec_znd_idfy_ctrlr_fpr(void* stream, xnvme_spec_znd_idfy_ctrlr* zctrlr, int opts)

    int xnvme_spec_znd_idfy_ctrlr_pr(xnvme_spec_znd_idfy_ctrlr* zctrlr, int opts)

    int xnvme_spec_znd_idfy_lbafe_fpr(void* stream, xnvme_spec_znd_idfy_lbafe* zonef, int opts)

    int xnvme_spec_znd_idfy_ns_fpr(void* stream, xnvme_spec_znd_idfy_ns* zns, int opts)

    int xnvme_spec_znd_idfy_ns_pr(xnvme_spec_znd_idfy_ns* zns, int opts)

    int xnvme_spec_znd_log_changes_fpr(void* stream, xnvme_spec_znd_log_changes* changes, int opts)

    int xnvme_spec_znd_log_changes_pr(xnvme_spec_znd_log_changes* changes, int opts)

    int xnvme_spec_znd_descr_fpr(void* stream, xnvme_spec_znd_descr* descr, int opts)

    int xnvme_spec_znd_descr_pr(xnvme_spec_znd_descr* descr, int opts)

    int xnvme_spec_znd_report_hdr_fpr(void* stream, xnvme_spec_znd_report_hdr* hdr, int opts)

    int xnvme_spec_znd_report_hdr_pr(xnvme_spec_znd_report_hdr* hdr, int opts)

    int xnvme_spec_znd_descr_fpr_yaml(void* stream, xnvme_spec_znd_descr* descr, int indent, char* sep)

    cdef struct xnvme_opts:
        char* be
        char* dev
        char* mem
        char* sync
        char* async_ "async"
        char* admin
        uint32_t nsid
        uint32_t create_mode
        uint8_t poll_io
        uint8_t poll_sq
        uint8_t register_files
        uint8_t register_buffers
        uint32_t use_cmb_sqs
        uint32_t shm_id
        uint32_t main_core
        char* core_mask
        char* adrfam
        uint32_t spdk_fabrics
        uint32_t oflags
        uint32_t rdonly
        uint32_t wronly
        uint32_t rdwr
        uint32_t create
        uint32_t truncate
        uint32_t direct
        uint32_t _rsvd
        uint32_t css__value "css.value"
        uint32_t css__given "css.given"

    xnvme_opts xnvme_opts_default()

    cdef struct xnvme_dev

    cpdef enum xnvme_enumerate_action:
        XNVME_ENUMERATE_DEV_KEEP_OPEN
        XNVME_ENUMERATE_DEV_CLOSE

    ctypedef int (*xnvme_enumerate_cb)(xnvme_dev* dev, void* cb_args)

    int xnvme_enumerate(char* sys_uri, xnvme_opts* opts, xnvme_enumerate_cb cb_func, void* cb_args)

    xnvme_dev* xnvme_dev_open(char* dev_uri, xnvme_opts* opts)

    void xnvme_dev_close(xnvme_dev* dev)

    void* xnvme_buf_alloc(xnvme_dev* dev, size_t nbytes)

    void* xnvme_buf_realloc(xnvme_dev* dev, void* buf, size_t nbytes)

    void xnvme_buf_free(xnvme_dev* dev, void* buf)

    cdef struct xnvme_queue

    cpdef enum xnvme_queue_opts:
        XNVME_QUEUE_IOPOLL
        XNVME_QUEUE_SQPOLL

    int xnvme_queue_init(xnvme_dev* dev, uint16_t capacity, int opts, xnvme_queue** queue)

    uint32_t xnvme_queue_get_capacity(xnvme_queue* queue)

    uint32_t xnvme_queue_get_outstanding(xnvme_queue* queue)

    int xnvme_queue_term(xnvme_queue* queue)

    int xnvme_queue_poke(xnvme_queue* queue, uint32_t max)

    int xnvme_queue_drain(xnvme_queue* queue)

    int xnvme_queue_wait(xnvme_queue* queue)

    xnvme_cmd_ctx* xnvme_queue_get_cmd_ctx(xnvme_queue* queue)

    int xnvme_queue_put_cmd_ctx(xnvme_queue* queue, xnvme_cmd_ctx* ctx)

    ctypedef void (*xnvme_queue_cb)(xnvme_cmd_ctx* ctx, void* opaque)

    cdef struct xnvme_cmd_ctx:
        xnvme_spec_cmd cmd
        xnvme_spec_cpl cpl
        xnvme_dev* dev
        uint32_t opts
        uint8_t be_rsvd[4]
        xnvme_queue* async__queue "async.queue"
        xnvme_queue_cb async__cb "async.cb"
        void* async__cb_arg "async.cb_arg"
        xnvme_cmd_ctx* link__sle_next "link.sle_next"

    void xnvme_cmd_ctx_set_cb(xnvme_cmd_ctx* ctx, xnvme_queue_cb cb, void* cb_arg)

    int xnvme_queue_set_cb(xnvme_queue* queue, xnvme_queue_cb cb, void* cb_arg)

    xnvme_cmd_ctx xnvme_cmd_ctx_from_dev(xnvme_dev* dev)

    xnvme_cmd_ctx* xnvme_cmd_ctx_from_queue(xnvme_queue* queue)

    void xnvme_cmd_ctx_clear(xnvme_cmd_ctx* ctx)

    int xnvme_cmd_ctx_cpl_status(xnvme_cmd_ctx* ctx)

    int xnvme_cmd_pass(xnvme_cmd_ctx* ctx, void* dbuf, size_t dbuf_nbytes, void* mbuf, size_t mbuf_nbytes)

    int xnvme_cmd_passv(xnvme_cmd_ctx* ctx, void* dvec, size_t dvec_cnt, size_t dvec_nbytes, void* mvec, size_t mvec_cnt, size_t mvec_nbytes)

    int xnvme_cmd_pass_admin(xnvme_cmd_ctx* ctx, void* dbuf, size_t dbuf_nbytes, void* mbuf, size_t mbuf_nbytes)
from libc.stdint cimport int8_t, uint16_t, int64_t, uint32_t, uint64_t, uint8_t

cdef extern from "libxnvme_nvm.h":

    cdef struct xnvme_be_attr:
        char* name
        uint8_t enabled
        uint8_t _rsvd[15]

    cdef struct xnvme_be_attr_list:
        uint32_t capacity
        int count
        xnvme_be_attr item[1]

    int xnvme_be_attr_list_bundled(xnvme_be_attr_list** list)

    cdef struct xnvme_dev

    xnvme_geo* xnvme_dev_get_geo(xnvme_dev* dev)

    xnvme_spec_idfy_ctrlr* xnvme_dev_get_ctrlr(xnvme_dev* dev)

    xnvme_spec_idfy_ctrlr* xnvme_dev_get_ctrlr_css(xnvme_dev* dev)

    xnvme_spec_idfy_ns* xnvme_dev_get_ns(xnvme_dev* dev)

    xnvme_spec_idfy_ns* xnvme_dev_get_ns_css(xnvme_dev* dev)

    uint32_t xnvme_dev_get_nsid(xnvme_dev* dev)

    uint8_t xnvme_dev_get_csi(xnvme_dev* dev)

    xnvme_ident* xnvme_dev_get_ident(xnvme_dev* dev)

    void* xnvme_dev_get_be_state(xnvme_dev* dev)

    uint64_t xnvme_dev_get_ssw(xnvme_dev* dev)

    void* xnvme_buf_phys_alloc(xnvme_dev* dev, size_t nbytes, uint64_t* phys)

    void xnvme_buf_phys_free(xnvme_dev* dev, void* buf)

    void* xnvme_buf_phys_realloc(xnvme_dev* dev, void* buf, size_t nbytes, uint64_t* phys)

    int xnvme_buf_vtophys(xnvme_dev* dev, void* buf, uint64_t* phys)

    void* xnvme_buf_virt_alloc(size_t alignment, size_t nbytes)

    void xnvme_buf_virt_free(void* buf)

    uint64_t XNVME_ILOG2(uint64_t x)

    int XNVME_MIN(int x, int y)

    uint64_t XNVME_MIN_U64(uint64_t x, uint64_t y)

    int64_t XNVME_MIN_S64(int64_t x, int64_t y)

    int XNVME_MAX(int x, int y)

    uint64_t _xnvme_timer_clock_sample()

    cdef struct xnvme_timer:
        uint64_t start
        uint64_t stop

    uint64_t xnvme_timer_start(xnvme_timer* t)

    uint64_t xnvme_timer_stop(xnvme_timer* t)

    double xnvme_timer_elapsed_secs(xnvme_timer* t)

    double xnvme_timer_elapsed(xnvme_timer* t)

    double xnvme_timer_elapsed_msecs(xnvme_timer* t)

    double xnvme_timer_elapsed_usecs(xnvme_timer* t)

    uint64_t xnvme_timer_elapsed_nsecs(xnvme_timer* t)

    void xnvme_timer_pr(xnvme_timer* t, char* prefix)

    void xnvme_timer_bw_pr(xnvme_timer* t, char* prefix, size_t nbytes)

    int xnvme_is_pow2(uint32_t val)

    cpdef enum xnvme_geo_type:
        XNVME_GEO_UNKNOWN
        XNVME_GEO_CONVENTIONAL
        XNVME_GEO_ZONED

    cdef struct xnvme_geo:
        xnvme_geo_type type
        uint32_t npugrp
        uint32_t npunit
        uint32_t nzone
        uint64_t nsect
        uint32_t nbytes
        uint32_t nbytes_oob
        uint64_t tbytes
        uint64_t ssw
        uint32_t mdts_nbytes
        uint32_t lba_nbytes
        uint8_t lba_extended
        uint8_t _rsvd[7]

    cdef struct xnvme_ident:
        char uri[384]
        uint32_t dtype
        uint32_t nsid
        uint8_t csi
        uint8_t rsvd[3]

    int xnvme_ident_from_uri(char* uri, xnvme_ident* ident)

    cdef struct xnvme_spec_ctrlr_bar:
        uint64_t cap
        uint32_t vs
        uint32_t intms
        uint32_t intmc
        uint32_t cc
        uint32_t rsvd24
        uint32_t csts
        uint32_t nssr
        uint32_t aqa
        uint64_t asq
        uint64_t acq
        uint32_t cmbloc
        uint32_t cmbsz
        uint32_t bpinfo
        uint32_t bprsel
        uint64_t bpmbl
        uint64_t cmbmsc
        uint32_t cmbsts
        uint8_t rsvd92[3492]
        uint32_t pmrcap
        uint32_t pmrctl
        uint32_t pmrsts
        uint32_t pmrebs
        uint32_t pmrswtp
        uint32_t pmrmscl
        uint32_t pmrmscu
        uint8_t css[484]

    cpdef enum xnvme_spec_status_code_type:
        XNVME_STATUS_CODE_TYPE_GENERIC
        XNVME_STATUS_CODE_TYPE_CMDSPEC
        XNVME_STATUS_CODE_TYPE_MEDIA
        XNVME_STATUS_CODE_TYPE_PATH
        XNVME_STATUS_CODE_TYPE_VENDOR

    cdef struct xnvme_spec_status:
        uint16_t val
        uint16_t p
        uint16_t sc
        uint16_t sct
        uint16_t rsvd2
        uint16_t m
        uint16_t dnr

    cdef struct xnvme_spec_cpl:
        uint16_t sqhd
        uint16_t sqid
        uint16_t cid
        xnvme_spec_status status
        uint64_t result
        uint32_t cdw0
        uint32_t rsvd1

    cdef struct xnvme_spec_log_health_entry:
        uint8_t crit_warn
        uint16_t comp_temp
        uint8_t avail_spare
        uint8_t avail_spare_thresh
        uint8_t pct_used
        uint8_t eg_crit_warn_sum
        uint8_t rsvd8[25]
        uint8_t data_units_read[16]
        uint8_t data_units_written[16]
        uint8_t host_read_cmds[16]
        uint8_t host_write_cmds[16]
        uint8_t ctrlr_busy_time[16]
        uint8_t pwr_cycles[16]
        uint8_t pwr_on_hours[16]
        uint8_t unsafe_shutdowns[16]
        uint8_t mdi_errs[16]
        uint8_t nr_err_logs[16]
        uint32_t warn_comp_temp_time
        uint32_t crit_comp_temp_time
        uint16_t temp_sens[8]
        uint32_t tmt1tc
        uint32_t tmt2tc
        uint32_t tttmt1
        uint32_t tttmt2
        uint8_t rsvd[280]

    cdef struct xnvme_spec_log_erri_entry:
        uint64_t ecnt
        uint16_t sqid
        uint16_t cid
        xnvme_spec_status status
        uint16_t eloc
        uint64_t lba
        uint32_t nsid
        uint8_t ven_si
        uint8_t trtype
        uint8_t reserved30[2]
        uint64_t cmd_si
        uint16_t trtype_si
        uint8_t reserved42[22]

    cpdef enum xnvme_spec_log_lpi:
        XNVME_SPEC_LOG_RSVD
        XNVME_SPEC_LOG_ERRI
        XNVME_SPEC_LOG_HEALTH
        XNVME_SPEC_LOG_FW
        XNVME_SPEC_LOG_CHNS
        XNVME_SPEC_LOG_CSAE
        XNVME_SPEC_LOG_SELFTEST
        XNVME_SPEC_LOG_TELEHOST
        XNVME_SPEC_LOG_TELECTRLR

    cpdef enum xnvme_spec_idfy_cns:
        XNVME_SPEC_IDFY_NS
        XNVME_SPEC_IDFY_CTRLR
        XNVME_SPEC_IDFY_NSLIST
        XNVME_SPEC_IDFY_NSDSCR
        XNVME_SPEC_IDFY_SETL
        XNVME_SPEC_IDFY_NS_IOCS
        XNVME_SPEC_IDFY_CTRLR_IOCS
        XNVME_SPEC_IDFY_NSLIST_IOCS
        XNVME_SPEC_IDFY_NSLIST_ALLOC
        XNVME_SPEC_IDFY_NS_ALLOC
        XNVME_SPEC_IDFY_CTRLR_NS
        XNVME_SPEC_IDFY_CTRLR_SUB
        XNVME_SPEC_IDFY_CTRLR_PRI
        XNVME_SPEC_IDFY_CTRLR_SEC
        XNVME_SPEC_IDFY_NSGRAN
        XNVME_SPEC_IDFY_UUIDL
        XNVME_SPEC_IDFY_NSLIST_ALLOC_IOCS
        XNVME_SPEC_IDFY_NS_ALLOC_IOCS
        XNVME_SPEC_IDFY_IOCS

    cdef struct xnvme_spec_lbaf:
        uint16_t ms
        uint8_t ds
        uint8_t rp
        uint8_t rsvd

    cpdef enum xnvme_spec_csi:
        XNVME_SPEC_CSI_NVM
        XNVME_SPEC_CSI_ZONED

    cdef struct xnvme_spec_idfy_ns:
        uint64_t nsze
        uint64_t ncap
        uint64_t nuse
        uint8_t nlbaf
        uint16_t nawun
        uint16_t nawupf
        uint16_t nacwu
        uint16_t nabsn
        uint16_t nabo
        uint16_t nabspf
        uint16_t noiob
        uint64_t nvmcap[2]
        uint8_t reserved64[40]
        uint8_t nguid[16]
        uint64_t eui64
        xnvme_spec_lbaf lbaf[16]
        uint8_t rsvd3776[3648]
        uint8_t vendor_specific[256]
        uint8_t nsfeat__thin_prov "nsfeat.thin_prov"
        uint8_t nsfeat__ns_atomic_write_unit "nsfeat.ns_atomic_write_unit"
        uint8_t nsfeat__dealloc_or_unwritten_error "nsfeat.dealloc_or_unwritten_error"
        uint8_t nsfeat__guid_never_reused "nsfeat.guid_never_reused"
        uint8_t nsfeat__reserved1 "nsfeat.reserved1"
        uint8_t flbas__format "flbas.format"
        uint8_t flbas__extended "flbas.extended"
        uint8_t flbas__reserved2 "flbas.reserved2"
        uint8_t mc__extended "mc.extended"
        uint8_t mc__pointer "mc.pointer"
        uint8_t mc__reserved3 "mc.reserved3"
        uint8_t dpc__val "dpc.val"
        uint8_t dpc__pit1 "dpc.pit1"
        uint8_t dpc__pit2 "dpc.pit2"
        uint8_t dpc__pit3 "dpc.pit3"
        uint8_t dpc__md_start "dpc.md_start"
        uint8_t dpc__md_end "dpc.md_end"
        uint8_t dps__val "dps.val"
        uint8_t dps__pit "dps.pit"
        uint8_t dps__md_start "dps.md_start"
        uint8_t dps__reserved4 "dps.reserved4"
        uint8_t nmic__can_share "nmic.can_share"
        uint8_t nmic__reserved "nmic.reserved"
        uint8_t nsrescap__val "nsrescap.val"
        uint8_t nsrescap__persist "nsrescap.persist"
        uint8_t nsrescap__write_exclusive "nsrescap.write_exclusive"
        uint8_t nsrescap__exclusive_access "nsrescap.exclusive_access"
        uint8_t nsrescap__write_exclusive_reg_only "nsrescap.write_exclusive_reg_only"
        uint8_t nsrescap__exclusive_access_reg_only "nsrescap.exclusive_access_reg_only"
        uint8_t nsrescap__write_exclusive_all_reg "nsrescap.write_exclusive_all_reg"
        uint8_t nsrescap__exclusive_access_all_reg "nsrescap.exclusive_access_all_reg"
        uint8_t nsrescap__ignore_existing_key "nsrescap.ignore_existing_key"
        uint8_t fpi__val "fpi.val"
        uint8_t fpi__percentage_remaining "fpi.percentage_remaining"
        uint8_t fpi__fpi_supported "fpi.fpi_supported"
        uint8_t dlfeat__val "dlfeat.val"
        uint8_t dlfeat__bits__read_value "dlfeat.bits.read_value"
        uint8_t dlfeat__bits__write_zero_deallocate "dlfeat.bits.write_zero_deallocate"
        uint8_t dlfeat__bits__guard_value "dlfeat.bits.guard_value"
        uint8_t dlfeat__bits__reserved "dlfeat.bits.reserved"

    cdef struct xnvme_spec_power_state:
        uint16_t mp
        uint8_t reserved1
        uint8_t mps
        uint8_t nops
        uint8_t reserved2
        uint32_t enlat
        uint32_t exlat
        uint8_t rrt
        uint8_t reserved3
        uint8_t rrl
        uint8_t reserved4
        uint8_t rwt
        uint8_t reserved5
        uint8_t rwl
        uint8_t reserved6
        uint8_t reserved7[16]

    cdef union xnvme_spec_vs_register:
        uint32_t val
        uint32_t bits__ter "bits.ter"
        uint32_t bits__mnr "bits.mnr"
        uint32_t bits__mjr "bits.mjr"

    cdef struct xnvme_spec_idfy_ctrlr:
        uint16_t vid
        uint16_t ssvid
        int8_t sn[20]
        int8_t mn[40]
        uint8_t fr[8]
        uint8_t rab
        uint8_t ieee[3]
        uint8_t mdts
        uint16_t cntlid
        xnvme_spec_vs_register ver
        uint32_t rtd3r
        uint32_t rtd3e
        uint8_t reserved_100[12]
        uint8_t fguid[16]
        uint8_t reserved_128[128]
        uint8_t acl
        uint8_t aerl
        uint8_t elpe
        uint8_t npss
        uint16_t wctemp
        uint16_t cctemp
        uint16_t mtfa
        uint32_t hmpre
        uint32_t hmmin
        uint64_t tnvmcap[2]
        uint64_t unvmcap[2]
        uint16_t edstt
        uint8_t fwug
        uint16_t kas
        uint16_t mntmt
        uint16_t mxtmt
        uint8_t reserved3[180]
        uint16_t maxcmd
        uint32_t nn
        uint16_t fuses
        uint16_t awun
        uint16_t awupf
        uint8_t nvscc
        uint8_t reserved531
        uint16_t acwu
        uint16_t reserved534
        uint32_t mnan
        uint8_t reserved4[224]
        uint8_t subnqn[256]
        uint8_t reserved5[768]
        xnvme_spec_power_state psd[32]
        uint8_t vs[1024]
        uint8_t cmic__val "cmic.val"
        uint8_t cmic__multi_port "cmic.multi_port"
        uint8_t cmic__multi_host "cmic.multi_host"
        uint8_t cmic__sr_iov "cmic.sr_iov"
        uint8_t cmic__reserved "cmic.reserved"
        uint32_t oaes__val "oaes.val"
        uint32_t oaes__reserved1 "oaes.reserved1"
        uint32_t oaes__ns_attribute_notices "oaes.ns_attribute_notices"
        uint32_t oaes__fw_activation_notices "oaes.fw_activation_notices"
        uint32_t oaes__reserved2 "oaes.reserved2"
        uint32_t oaes__zone_changes "oaes.zone_changes"
        uint32_t oaes__reserved3 "oaes.reserved3"
        uint32_t ctratt__val "ctratt.val"
        uint32_t ctratt__host_id_exhid_supported "ctratt.host_id_exhid_supported"
        uint32_t ctratt__non_operational_power_state_permissive_mode "ctratt.non_operational_power_state_permissive_mode"
        uint32_t ctratt__reserved "ctratt.reserved"
        uint16_t oacs__val "oacs.val"
        uint16_t oacs__security "oacs.security"
        uint16_t oacs__format "oacs.format"
        uint16_t oacs__firmware "oacs.firmware"
        uint16_t oacs__ns_manage "oacs.ns_manage"
        uint16_t oacs__device_self_test "oacs.device_self_test"
        uint16_t oacs__directives "oacs.directives"
        uint16_t oacs__nvme_mi "oacs.nvme_mi"
        uint16_t oacs__virtualization_management "oacs.virtualization_management"
        uint16_t oacs__doorbell_buffer_config "oacs.doorbell_buffer_config"
        uint16_t oacs__oacs_rsvd "oacs.oacs_rsvd"
        uint8_t frmw__val "frmw.val"
        uint8_t frmw__slot1_ro "frmw.slot1_ro"
        uint8_t frmw__num_slots "frmw.num_slots"
        uint8_t frmw__activation_without_reset "frmw.activation_without_reset"
        uint8_t frmw__frmw_rsvd "frmw.frmw_rsvd"
        uint8_t lpa__val "lpa.val"
        uint8_t lpa__ns_smart "lpa.ns_smart"
        uint8_t lpa__celp "lpa.celp"
        uint8_t lpa__edlp "lpa.edlp"
        uint8_t lpa__telemetry "lpa.telemetry"
        uint8_t lpa__pel "lpa.pel"
        uint8_t lpa__lpa_rsvd "lpa.lpa_rsvd"
        uint8_t avscc__val "avscc.val"
        uint8_t avscc__spec_format "avscc.spec_format"
        uint8_t avscc__avscc_rsvd "avscc.avscc_rsvd"
        uint8_t apsta__val "apsta.val"
        uint8_t apsta__supported "apsta.supported"
        uint8_t apsta__apsta_rsvd "apsta.apsta_rsvd"
        uint32_t rpmbs__val "rpmbs.val"
        uint8_t rpmbs__num_rpmb_units "rpmbs.num_rpmb_units"
        uint8_t rpmbs__auth_method "rpmbs.auth_method"
        uint8_t rpmbs__reserved1 "rpmbs.reserved1"
        uint8_t rpmbs__reserved2 "rpmbs.reserved2"
        uint8_t rpmbs__total_size "rpmbs.total_size"
        uint8_t rpmbs__access_size "rpmbs.access_size"
        uint8_t dsto__val "dsto.val"
        uint8_t dsto__bits__one_only "dsto.bits.one_only"
        uint8_t dsto__bits__reserved "dsto.bits.reserved"
        uint16_t hctma__val "hctma.val"
        uint16_t hctma__bits__supported "hctma.bits.supported"
        uint16_t hctma__bits__reserved "hctma.bits.reserved"
        uint32_t sanicap__val "sanicap.val"
        uint32_t sanicap__bits__crypto_erase "sanicap.bits.crypto_erase"
        uint32_t sanicap__bits__block_erase "sanicap.bits.block_erase"
        uint32_t sanicap__bits__overwrite "sanicap.bits.overwrite"
        uint32_t sanicap__bits__reserved "sanicap.bits.reserved"
        uint8_t sqes__val "sqes.val"
        uint8_t sqes__min "sqes.min"
        uint8_t sqes__max "sqes.max"
        uint8_t cqes__val "cqes.val"
        uint8_t cqes__min "cqes.min"
        uint8_t cqes__max "cqes.max"
        uint16_t oncs__val "oncs.val"
        uint16_t oncs__compare "oncs.compare"
        uint16_t oncs__write_unc "oncs.write_unc"
        uint16_t oncs__dsm "oncs.dsm"
        uint16_t oncs__write_zeroes "oncs.write_zeroes"
        uint16_t oncs__set_features_save "oncs.set_features_save"
        uint16_t oncs__reservations "oncs.reservations"
        uint16_t oncs__timestamp "oncs.timestamp"
        uint16_t oncs__reserved "oncs.reserved"
        uint8_t fna__val "fna.val"
        uint8_t fna__format_all_ns "fna.format_all_ns"
        uint8_t fna__erase_all_ns "fna.erase_all_ns"
        uint8_t fna__crypto_erase_supported "fna.crypto_erase_supported"
        uint8_t fna__reserved "fna.reserved"
        uint8_t vwc__val "vwc.val"
        uint8_t vwc__present "vwc.present"
        uint8_t vwc__flush_broadcast "vwc.flush_broadcast"
        uint8_t vwc__reserved "vwc.reserved"
        uint32_t sgls__val "sgls.val"
        uint32_t sgls__supported "sgls.supported"
        uint32_t sgls__keyed_sgl "sgls.keyed_sgl"
        uint32_t sgls__reserved1 "sgls.reserved1"
        uint32_t sgls__bit_bucket_descriptor "sgls.bit_bucket_descriptor"
        uint32_t sgls__metadata_pointer "sgls.metadata_pointer"
        uint32_t sgls__oversized_sgl "sgls.oversized_sgl"
        uint32_t sgls__metadata_address "sgls.metadata_address"
        uint32_t sgls__sgl_offset "sgls.sgl_offset"
        uint32_t sgls__transport_sgl "sgls.transport_sgl"
        uint32_t sgls__reserved2 "sgls.reserved2"
        uint32_t nvmf_specific__ioccsz "nvmf_specific.ioccsz"
        uint32_t nvmf_specific__iorcsz "nvmf_specific.iorcsz"
        uint16_t nvmf_specific__icdoff "nvmf_specific.icdoff"
        uint8_t nvmf_specific__msdbd "nvmf_specific.msdbd"
        uint8_t nvmf_specific__reserved "nvmf_specific.reserved[244]"
        uint8_t nvmf_specific__ctrattr__ctrlr_model "nvmf_specific.ctrattr.ctrlr_model"
        uint8_t nvmf_specific__ctrattr__reserved "nvmf_specific.ctrattr.reserved"

    cdef struct xnvme_spec_cs_vector:
        uint64_t val
        uint64_t nvm
        uint64_t rsvd1
        uint64_t zns
        uint64_t rsvd

    cdef struct xnvme_spec_idfy_cs:
        xnvme_spec_cs_vector iocsc[512]

    cdef struct xnvme_spec_idfy:
        xnvme_spec_idfy_ctrlr ctrlr
        xnvme_spec_idfy_ns ns
        xnvme_spec_idfy_cs cs

    cpdef enum xnvme_spec_adm_opc:
        XNVME_SPEC_ADM_OPC_LOG
        XNVME_SPEC_ADM_OPC_IDFY
        XNVME_SPEC_ADM_OPC_SFEAT
        XNVME_SPEC_ADM_OPC_GFEAT

    cpdef enum xnvme_spec_nvm_opc:
        XNVME_SPEC_NVM_OPC_FLUSH
        XNVME_SPEC_NVM_OPC_WRITE
        XNVME_SPEC_NVM_OPC_READ
        XNVME_SPEC_NVM_OPC_WRITE_UNCORRECTABLE
        XNVME_SPEC_NVM_OPC_WRITE_ZEROES
        XNVME_SPEC_NVM_OPC_SCOPY
        XNVME_SPEC_NVM_OPC_FMT
        XNVME_SPEC_NVM_OPC_SANITIZE

    cpdef enum xnvme_spec_feat_id:
        XNVME_SPEC_FEAT_ARBITRATION
        XNVME_SPEC_FEAT_PWR_MGMT
        XNVME_SPEC_FEAT_LBA_RANGETYPE
        XNVME_SPEC_FEAT_TEMP_THRESHOLD
        XNVME_SPEC_FEAT_ERROR_RECOVERY
        XNVME_SPEC_FEAT_VWCACHE
        XNVME_SPEC_FEAT_NQUEUES

    cpdef enum xnvme_spec_feat_sel:
        XNVME_SPEC_FEAT_SEL_CURRENT
        XNVME_SPEC_FEAT_SEL_DEFAULT
        XNVME_SPEC_FEAT_SEL_SAVED
        XNVME_SPEC_FEAT_SEL_SUPPORTED

    cdef struct xnvme_spec_feat:
        uint32_t val
        uint32_t temp_threshold__tmpth "temp_threshold.tmpth"
        uint32_t temp_threshold__tmpsel "temp_threshold.tmpsel"
        uint32_t temp_threshold__thsel "temp_threshold.thsel"
        uint32_t error_recovery__tler "error_recovery.tler"
        uint32_t error_recovery__dulbe "error_recovery.dulbe"
        uint32_t error_recovery__rsvd "error_recovery.rsvd"
        uint32_t nqueues__nsqa "nqueues.nsqa"
        uint32_t nqueues__ncqa "nqueues.ncqa"

    cdef struct xnvme_spec_dsm_range:
        uint32_t cattr
        uint32_t nlb
        uint64_t slba

    cpdef enum xnvme_spec_flag:
        XNVME_SPEC_FLAG_LIMITED_RETRY
        XNVME_SPEC_FLAG_FORCE_UNIT_ACCESS
        XNVME_SPEC_FLAG_PRINFO_PRCHK_REF
        XNVME_SPEC_FLAG_PRINFO_PRCHK_APP
        XNVME_SPEC_FLAG_PRINFO_PRCHK_GUARD
        XNVME_SPEC_FLAG_PRINFO_PRACT

    cpdef enum xnvme_nvme_sgl_descriptor_type:
        XNVME_SPEC_SGL_DESCR_TYPE_DATA_BLOCK
        XNVME_SPEC_SGL_DESCR_TYPE_BIT_BUCKET
        XNVME_SPEC_SGL_DESCR_TYPE_SEGMENT
        XNVME_SPEC_SGL_DESCR_TYPE_LAST_SEGMENT
        XNVME_SPEC_SGL_DESCR_TYPE_KEYED_DATA_BLOCK
        XNVME_SPEC_SGL_DESCR_TYPE_VENDOR_SPECIFIC

    cpdef enum xnvme_spec_sgl_descriptor_subtype:
        XNVME_SPEC_SGL_DESCR_SUBTYPE_ADDRESS
        XNVME_SPEC_SGL_DESCR_SUBTYPE_OFFSET

    cdef struct xnvme_spec_sgl_descriptor:
        uint64_t addr
        uint64_t generic__rsvd "generic.rsvd"
        uint64_t generic__subtype "generic.subtype"
        uint64_t generic__type "generic.type"
        uint64_t unkeyed__len "unkeyed.len"
        uint64_t unkeyed__rsvd "unkeyed.rsvd"
        uint64_t unkeyed__subtype "unkeyed.subtype"
        uint64_t unkeyed__type "unkeyed.type"

    cpdef enum xnvme_spec_psdt:
        XNVME_SPEC_PSDT_PRP
        XNVME_SPEC_PSDT_SGL_MPTR_CONTIGUOUS
        XNVME_SPEC_PSDT_SGL_MPTR_SGL

    cdef struct xnvme_spec_cmd_common:
        uint16_t opcode
        uint16_t fuse
        uint16_t rsvd
        uint16_t psdt
        uint16_t cid
        uint32_t nsid
        uint32_t cdw02
        uint32_t cdw03
        uint64_t mptr
        uint32_t ndt
        uint32_t ndm
        uint32_t cdw12
        uint32_t cdw13
        uint32_t cdw14
        uint32_t cdw15
        xnvme_spec_sgl_descriptor dptr__sgl "dptr.sgl"
        uint64_t dptr__prp__prp1 "dptr.prp.prp1"
        uint64_t dptr__prp__prp2 "dptr.prp.prp2"
        uint64_t dptr__lnx_ioctl__data "dptr.lnx_ioctl.data"
        uint32_t dptr__lnx_ioctl__metadata_len "dptr.lnx_ioctl.metadata_len"
        uint32_t dptr__lnx_ioctl__data_len "dptr.lnx_ioctl.data_len"

    cdef struct xnvme_spec_cmd_sanitize:
        uint32_t cdw00_09[10]
        uint32_t sanact
        uint32_t ause
        uint32_t owpass
        uint32_t oipbp
        uint32_t nodas
        uint32_t rsvd
        uint32_t ovrpat
        uint32_t cdw12_15[4]

    cdef struct xnvme_spec_cmd_format:
        uint32_t cdw00_09[10]
        uint32_t lbaf
        uint32_t mset
        uint32_t pi
        uint32_t pil
        uint32_t ses
        uint32_t zf
        uint32_t rsvd
        uint32_t cdw11_15[5]

    cdef struct xnvme_spec_cmd_gfeat:
        uint32_t cdw00_09[10]
        uint32_t cdw11_15[5]
        uint32_t cdw10__val "cdw10.val"
        uint32_t cdw10__fid "cdw10.fid"
        uint32_t cdw10__sel "cdw10.sel"
        uint32_t cdw10__rsvd10 "cdw10.rsvd10"

    cdef struct xnvme_spec_cmd_sfeat:
        uint32_t cdw00_09[10]
        xnvme_spec_feat feat
        uint32_t cdw12_15[4]
        uint32_t cdw10__val "cdw10.val"
        uint32_t cdw10__fid "cdw10.fid"
        uint32_t cdw10__rsvd10 "cdw10.rsvd10"
        uint32_t cdw10__save "cdw10.save"

    cdef struct xnvme_spec_cmd_idfy:
        uint32_t cdw00_09[10]
        uint32_t cns
        uint32_t rsvd1
        uint32_t cntid
        uint32_t nvmsetid
        uint32_t rsvd2
        uint32_t csi
        uint32_t cdw12_13[2]
        uint32_t uuid
        uint32_t rsvd3
        uint32_t cdw15

    cdef struct xnvme_spec_cmd_log:
        uint32_t cdw00_09[10]
        uint32_t lid
        uint32_t lsp
        uint32_t rsvd10
        uint32_t rae
        uint32_t numdl
        uint32_t numdu
        uint32_t rsvd11
        uint32_t lpol
        uint32_t lpou
        uint32_t cdw14_15[2]

    cdef struct xnvme_spec_cmd_nvm:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd
        uint32_t dtype
        uint32_t rsvd2
        uint32_t prinfo
        uint32_t fua
        uint32_t lr
        uint32_t cdw13_15[3]

    cdef struct xnvme_spec_nvm_write_zeroes:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd1
        uint32_t deac
        uint32_t prinfo
        uint32_t fua
        uint32_t lr
        uint32_t cdw_13
        uint32_t ilbrt
        uint32_t lbat
        uint32_t lbatm

    cpdef enum xnvme_spec_nvm_cmd_cpl_sc:
        XNVME_SPEC_NVM_CMD_CPL_SC_WRITE_TO_RONLY

    cdef struct xnvme_spec_nvm_scopy_fmt_zero:
        uint8_t rsvd0[8]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd20
        uint32_t eilbrt
        uint32_t elbatm
        uint32_t elbat

    cpdef enum xnvme_nvm_scopy_fmt:
        XNVME_NVM_SCOPY_FMT_ZERO
        XNVME_NVM_SCOPY_FMT_SRCLEN

    cdef struct xnvme_spec_nvm_scopy_source_range:
        xnvme_spec_nvm_scopy_fmt_zero entry[128]

    cdef struct xnvme_spec_nvm_cmd_scopy:
        uint32_t cdw00_09[10]
        uint64_t sdlba
        uint32_t nr
        uint32_t df
        uint32_t prinfor
        uint32_t rsvd1
        uint32_t dtype
        uint32_t rsvd2
        uint32_t prinfow
        uint32_t fua
        uint32_t lr
        uint32_t rsvd3
        uint32_t dspec
        uint32_t ilbrt
        uint32_t lbat
        uint32_t lbatm

    cdef struct xnvme_spec_nvm_cmd_scopy_fmt_srclen:
        uint64_t start
        uint64_t len

    cdef struct xnvme_spec_nvm_cmd:
        xnvme_spec_nvm_cmd_scopy scopy

    cdef struct xnvme_spec_nvm_idfy_ctrlr:
        uint8_t byte0_519[520]
        uint8_t byte522_533[12]
        uint8_t byte536_4095[3559]
        uint16_t oncs__val "oncs.val"
        uint16_t oncs__compare "oncs.compare"
        uint16_t oncs__write_unc "oncs.write_unc"
        uint16_t oncs__dsm "oncs.dsm"
        uint16_t oncs__write_zeroes "oncs.write_zeroes"
        uint16_t oncs__set_features_save "oncs.set_features_save"
        uint16_t oncs__reservations "oncs.reservations"
        uint16_t oncs__timestamp "oncs.timestamp"
        uint16_t oncs__verify "oncs.verify"
        uint16_t oncs__copy "oncs.copy"
        uint16_t oncs__reserved "oncs.reserved"
        uint16_t ocfs__val "ocfs.val"
        uint16_t ocfs__copy_fmt0 "ocfs.copy_fmt0"
        uint16_t ocfs__rsvd "ocfs.rsvd"

    cdef struct xnvme_spec_nvm_idfy_ns:
        uint8_t byte0_73[74]
        uint16_t mssrl
        uint32_t mcl
        uint8_t msrc
        uint8_t byte81_4095[4014]

    cdef struct xnvme_spec_nvm_idfy:
        xnvme_spec_idfy base
        xnvme_spec_nvm_idfy_ctrlr ctrlr
        xnvme_spec_nvm_idfy_ns ns

    cpdef enum xnvme_spec_znd_log_lid:
        XNVME_SPEC_LOG_ZND_CHANGES

    cpdef enum xnvme_spec_znd_opc:
        XNVME_SPEC_ZND_OPC_MGMT_SEND
        XNVME_SPEC_ZND_OPC_MGMT_RECV
        XNVME_SPEC_ZND_OPC_APPEND

    cdef struct xnvme_spec_znd_cmd_mgmt_send:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nrange
        uint32_t zsa
        uint32_t select_all
        uint32_t zsaso
        uint32_t rsvd
        uint32_t cdw14_15[2]

    cdef struct xnvme_spec_znd_cmd_mgmt_recv:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t ndwords
        uint32_t zra
        uint32_t zrasf
        uint32_t partial
        uint32_t rsvd
        uint64_t addrs_dst

    cdef struct xnvme_spec_znd_cmd_append:
        uint32_t cdw00_09[10]
        uint64_t zslba
        uint32_t nlb
        uint32_t rsvd
        uint32_t dtype
        uint32_t prinfo
        uint32_t rsvd2
        uint32_t fua
        uint32_t lr
        uint32_t cdw13_15[3]

    cdef struct xnvme_spec_znd_cmd:
        xnvme_spec_znd_cmd_mgmt_send mgmt_send
        xnvme_spec_znd_cmd_mgmt_recv mgmt_recv
        xnvme_spec_znd_cmd_append append

    cdef struct xnvme_spec_cmd:
        xnvme_spec_cmd_common common
        xnvme_spec_cmd_sanitize sanitize
        xnvme_spec_cmd_format format
        xnvme_spec_cmd_log log
        xnvme_spec_cmd_gfeat gfeat
        xnvme_spec_cmd_sfeat sfeat
        xnvme_spec_cmd_idfy idfy
        xnvme_spec_cmd_nvm nvm
        xnvme_spec_nvm_cmd_scopy scopy
        xnvme_spec_nvm_write_zeroes write_zeroes
        xnvme_spec_znd_cmd znd

    cpdef enum xnvme_spec_znd_status_code:
        XNVME_SPEC_ZND_SC_INVALID_FORMAT
        XNVME_SPEC_ZND_SC_INVALID_ZONE_OP
        XNVME_SPEC_ZND_SC_NOZRWA
        XNVME_SPEC_ZND_SC_BOUNDARY_ERROR
        XNVME_SPEC_ZND_SC_IS_FULL
        XNVME_SPEC_ZND_SC_IS_READONLY
        XNVME_SPEC_ZND_SC_IS_OFFLINE
        XNVME_SPEC_ZND_SC_INVALID_WRITE
        XNVME_SPEC_ZND_SC_TOO_MANY_ACTIVE
        XNVME_SPEC_ZND_SC_TOO_MANY_OPEN
        XNVME_SPEC_ZND_SC_INVALID_TRANS

    cpdef enum xnvme_spec_znd_mgmt_send_action_so:
        XNVME_SPEC_ZND_MGMT_OPEN_WITH_ZRWA

    cpdef enum xnvme_spec_znd_cmd_mgmt_send_action:
        XNVME_SPEC_ZND_CMD_MGMT_SEND_CLOSE
        XNVME_SPEC_ZND_CMD_MGMT_SEND_FINISH
        XNVME_SPEC_ZND_CMD_MGMT_SEND_OPEN
        XNVME_SPEC_ZND_CMD_MGMT_SEND_RESET
        XNVME_SPEC_ZND_CMD_MGMT_SEND_OFFLINE
        XNVME_SPEC_ZND_CMD_MGMT_SEND_DESCRIPTOR
        XNVME_SPEC_ZND_CMD_MGMT_SEND_FLUSH

    cpdef enum xnvme_spec_znd_cmd_mgmt_recv_action_sf:
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_ALL
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_EMPTY
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_IOPEN
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_EOPEN
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_CLOSED
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_FULL
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_RONLY
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_OFFLINE

    cpdef enum xnvme_spec_znd_cmd_mgmt_recv_action:
        XNVME_SPEC_ZND_CMD_MGMT_RECV_ACTION_REPORT
        XNVME_SPEC_ZND_CMD_MGMT_RECV_ACTION_REPORT_EXTENDED

    cpdef enum xnvme_spec_znd_type:
        XNVME_SPEC_ZND_TYPE_SEQWR

    cpdef enum xnvme_spec_znd_state:
        XNVME_SPEC_ZND_STATE_EMPTY
        XNVME_SPEC_ZND_STATE_IOPEN
        XNVME_SPEC_ZND_STATE_EOPEN
        XNVME_SPEC_ZND_STATE_CLOSED
        XNVME_SPEC_ZND_STATE_RONLY
        XNVME_SPEC_ZND_STATE_FULL
        XNVME_SPEC_ZND_STATE_OFFLINE

    cdef struct xnvme_spec_znd_idfy_ctrlr:
        uint8_t zasl
        uint8_t rsvd8[4095]

    cdef struct xnvme_spec_znd_idfy_lbafe:
        uint64_t zsze
        uint8_t zdes
        uint8_t rsvd[7]

    cdef struct xnvme_spec_znd_idfy_ns:
        uint32_t mar
        uint32_t mor
        uint32_t rrl
        uint32_t frl
        uint8_t rsvd12[24]
        uint32_t numzrwa
        uint16_t zrwafg
        uint16_t zrwas
        uint8_t rsvd53[2763]
        xnvme_spec_znd_idfy_lbafe lbafe[16]
        uint8_t rsvd3072[768]
        uint8_t vs[256]
        uint16_t zoc__val "zoc.val"
        uint16_t zoc__bits__vzcap "zoc.bits.vzcap"
        uint16_t zoc__bits__zae "zoc.bits.zae"
        uint16_t zoc__bits__rsvd "zoc.bits.rsvd"
        uint16_t ozcs__val "ozcs.val"
        uint16_t ozcs__bits__razb "ozcs.bits.razb"
        uint16_t ozcs__bits__zrwasup "ozcs.bits.zrwasup"
        uint16_t ozcs__bits__rsvd "ozcs.bits.rsvd"
        uint8_t zrwacap__val "zrwacap.val"
        uint8_t zrwacap__bits__expflushsup "zrwacap.bits.expflushsup"
        uint8_t zrwacap__bits__rsvd0 "zrwacap.bits.rsvd0"

    cdef struct xnvme_spec_znd_idfy:
        xnvme_spec_idfy base
        xnvme_spec_znd_idfy_ctrlr zctrlr
        xnvme_spec_znd_idfy_ns zns

    cdef struct xnvme_spec_znd_log_changes:
        uint16_t nidents
        uint8_t rsvd2[6]
        uint64_t idents[511]

    cdef struct xnvme_spec_znd_descr:
        uint8_t zt
        uint8_t rsvd0
        uint8_t rsvd1
        uint8_t zs
        uint8_t rsvd7[5]
        uint64_t zcap
        uint64_t zslba
        uint64_t wp
        uint8_t rsvd63[32]
        uint8_t za__val "za.val"
        uint8_t za__zfc "za.zfc"
        uint8_t za__zfr "za.zfr"
        uint8_t za__rzr "za.rzr"
        uint8_t za__zrwav "za.zrwav"
        uint8_t za__rsvd3 "za.rsvd3"
        uint8_t za__zdev "za.zdev"

    cdef struct xnvme_spec_znd_report_hdr:
        uint64_t nzones
        uint8_t rsvd[56]

    int xnvme_spec_log_health_fpr(void* stream, xnvme_spec_log_health_entry* log, int opts)

    int xnvme_spec_log_health_pr(xnvme_spec_log_health_entry* log, int opts)

    int xnvme_spec_log_erri_fpr(void* stream, xnvme_spec_log_erri_entry* log, int limit, int opts)

    int xnvme_spec_log_erri_pr(xnvme_spec_log_erri_entry* log, int limit, int opts)

    int xnvme_spec_idfy_ns_fpr(void* stream, xnvme_spec_idfy_ns* idfy, int opts)

    int xnvme_spec_idfy_ns_pr(xnvme_spec_idfy_ns* idfy, int opts)

    int xnvme_spec_idfy_ctrl_fpr(void* stream, xnvme_spec_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_idfy_ctrl_pr(xnvme_spec_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_idfy_cs_fpr(void* stream, xnvme_spec_idfy_cs* idfy, int opts)

    int xnvme_spec_idfy_cs_pr(xnvme_spec_idfy_cs* idfy, int opts)

    int xnvme_spec_feat_fpr(void* stream, uint8_t fid, xnvme_spec_feat feat, int opts)

    int xnvme_spec_feat_pr(uint8_t fid, xnvme_spec_feat feat, int opts)

    int xnvme_spec_cmd_fpr(void* stream, xnvme_spec_cmd* cmd, int opts)

    int xnvme_spec_cmd_pr(xnvme_spec_cmd* cmd, int opts)

    int xnvme_spec_nvm_scopy_fmt_zero_fpr(void* stream, xnvme_spec_nvm_scopy_fmt_zero* entry, int opts)

    int xnvme_spec_nvm_scopy_fmt_zero_pr(xnvme_spec_nvm_scopy_fmt_zero* entry, int opts)

    int xnvme_spec_nvm_scopy_source_range_fpr(void* stream, xnvme_spec_nvm_scopy_source_range* srange, uint8_t nr, int opts)

    int xnvme_spec_nvm_scopy_source_range_pr(xnvme_spec_nvm_scopy_source_range* srange, uint8_t nr, int opts)

    int xnvme_spec_idfy_ctrlr_fpr(void* stream, xnvme_spec_nvm_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_nvm_idfy_ctrlr_pr(xnvme_spec_nvm_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_nvm_idfy_ns_fpr(void* stream, xnvme_spec_nvm_idfy_ns* idfy, int opts)

    int xnvme_spec_nvm_idfy_ns_pr(xnvme_spec_nvm_idfy_ns* idfy, int opts)

    int xnvme_spec_znd_idfy_ctrlr_fpr(void* stream, xnvme_spec_znd_idfy_ctrlr* zctrlr, int opts)

    int xnvme_spec_znd_idfy_ctrlr_pr(xnvme_spec_znd_idfy_ctrlr* zctrlr, int opts)

    int xnvme_spec_znd_idfy_lbafe_fpr(void* stream, xnvme_spec_znd_idfy_lbafe* zonef, int opts)

    int xnvme_spec_znd_idfy_ns_fpr(void* stream, xnvme_spec_znd_idfy_ns* zns, int opts)

    int xnvme_spec_znd_idfy_ns_pr(xnvme_spec_znd_idfy_ns* zns, int opts)

    int xnvme_spec_znd_log_changes_fpr(void* stream, xnvme_spec_znd_log_changes* changes, int opts)

    int xnvme_spec_znd_log_changes_pr(xnvme_spec_znd_log_changes* changes, int opts)

    int xnvme_spec_znd_descr_fpr(void* stream, xnvme_spec_znd_descr* descr, int opts)

    int xnvme_spec_znd_descr_pr(xnvme_spec_znd_descr* descr, int opts)

    int xnvme_spec_znd_report_hdr_fpr(void* stream, xnvme_spec_znd_report_hdr* hdr, int opts)

    int xnvme_spec_znd_report_hdr_pr(xnvme_spec_znd_report_hdr* hdr, int opts)

    int xnvme_spec_znd_descr_fpr_yaml(void* stream, xnvme_spec_znd_descr* descr, int indent, char* sep)

    cdef struct xnvme_opts:
        char* be
        char* dev
        char* mem
        char* sync
        char* async_ "async"
        char* admin
        uint32_t nsid
        uint32_t create_mode
        uint8_t poll_io
        uint8_t poll_sq
        uint8_t register_files
        uint8_t register_buffers
        uint32_t use_cmb_sqs
        uint32_t shm_id
        uint32_t main_core
        char* core_mask
        char* adrfam
        uint32_t spdk_fabrics
        uint32_t oflags
        uint32_t rdonly
        uint32_t wronly
        uint32_t rdwr
        uint32_t create
        uint32_t truncate
        uint32_t direct
        uint32_t _rsvd
        uint32_t css__value "css.value"
        uint32_t css__given "css.given"

    xnvme_opts xnvme_opts_default()

    cdef struct xnvme_dev

    cpdef enum xnvme_enumerate_action:
        XNVME_ENUMERATE_DEV_KEEP_OPEN
        XNVME_ENUMERATE_DEV_CLOSE

    ctypedef int (*xnvme_enumerate_cb)(xnvme_dev* dev, void* cb_args)

    int xnvme_enumerate(char* sys_uri, xnvme_opts* opts, xnvme_enumerate_cb cb_func, void* cb_args)

    xnvme_dev* xnvme_dev_open(char* dev_uri, xnvme_opts* opts)

    void xnvme_dev_close(xnvme_dev* dev)

    void* xnvme_buf_alloc(xnvme_dev* dev, size_t nbytes)

    void* xnvme_buf_realloc(xnvme_dev* dev, void* buf, size_t nbytes)

    void xnvme_buf_free(xnvme_dev* dev, void* buf)

    cdef struct xnvme_queue

    cpdef enum xnvme_queue_opts:
        XNVME_QUEUE_IOPOLL
        XNVME_QUEUE_SQPOLL

    int xnvme_queue_init(xnvme_dev* dev, uint16_t capacity, int opts, xnvme_queue** queue)

    uint32_t xnvme_queue_get_capacity(xnvme_queue* queue)

    uint32_t xnvme_queue_get_outstanding(xnvme_queue* queue)

    int xnvme_queue_term(xnvme_queue* queue)

    int xnvme_queue_poke(xnvme_queue* queue, uint32_t max)

    int xnvme_queue_drain(xnvme_queue* queue)

    int xnvme_queue_wait(xnvme_queue* queue)

    xnvme_cmd_ctx* xnvme_queue_get_cmd_ctx(xnvme_queue* queue)

    int xnvme_queue_put_cmd_ctx(xnvme_queue* queue, xnvme_cmd_ctx* ctx)

    ctypedef void (*xnvme_queue_cb)(xnvme_cmd_ctx* ctx, void* opaque)

    cdef struct xnvme_cmd_ctx:
        xnvme_spec_cmd cmd
        xnvme_spec_cpl cpl
        xnvme_dev* dev
        uint32_t opts
        uint8_t be_rsvd[4]
        xnvme_queue* async__queue "async.queue"
        xnvme_queue_cb async__cb "async.cb"
        void* async__cb_arg "async.cb_arg"
        xnvme_cmd_ctx* link__sle_next "link.sle_next"

    void xnvme_cmd_ctx_set_cb(xnvme_cmd_ctx* ctx, xnvme_queue_cb cb, void* cb_arg)

    int xnvme_queue_set_cb(xnvme_queue* queue, xnvme_queue_cb cb, void* cb_arg)

    xnvme_cmd_ctx xnvme_cmd_ctx_from_dev(xnvme_dev* dev)

    xnvme_cmd_ctx* xnvme_cmd_ctx_from_queue(xnvme_queue* queue)

    void xnvme_cmd_ctx_clear(xnvme_cmd_ctx* ctx)

    int xnvme_cmd_ctx_cpl_status(xnvme_cmd_ctx* ctx)

    int xnvme_cmd_pass(xnvme_cmd_ctx* ctx, void* dbuf, size_t dbuf_nbytes, void* mbuf, size_t mbuf_nbytes)

    int xnvme_cmd_passv(xnvme_cmd_ctx* ctx, void* dvec, size_t dvec_cnt, size_t dvec_nbytes, void* mvec, size_t mvec_cnt, size_t mvec_nbytes)

    int xnvme_cmd_pass_admin(xnvme_cmd_ctx* ctx, void* dbuf, size_t dbuf_nbytes, void* mbuf, size_t mbuf_nbytes)

    int xnvme_nvm_read(xnvme_cmd_ctx* ctx, uint32_t nsid, uint64_t slba, uint16_t nlb, void* dbuf, void* mbuf)

    int xnvme_nvm_write(xnvme_cmd_ctx* ctx, uint32_t nsid, uint64_t slba, uint16_t nlb, void* dbuf, void* mbuf)

    int xnvme_nvm_write_uncorrectable(xnvme_cmd_ctx* ctx, uint32_t nsid, uint64_t slba, uint16_t nlb)

    int xnvme_nvm_write_zeroes(xnvme_cmd_ctx* ctx, uint32_t nsid, uint64_t sdlba, uint16_t nlb)

    int xnvme_nvm_scopy(xnvme_cmd_ctx* ctx, uint32_t nsid, uint64_t sdlba, xnvme_spec_nvm_scopy_fmt_zero* ranges, uint8_t nr, xnvme_nvm_scopy_fmt copy_fmt)
from libc.stdint cimport int8_t, uint16_t, int64_t, uint32_t, uint64_t, uint8_t

cdef extern from "libxnvme_pp.h":

    cdef struct xnvme_be_attr:
        char* name
        uint8_t enabled
        uint8_t _rsvd[15]

    cdef struct xnvme_be_attr_list:
        uint32_t capacity
        int count
        xnvme_be_attr item[1]

    int xnvme_be_attr_list_bundled(xnvme_be_attr_list** list)

    cdef struct xnvme_dev

    xnvme_geo* xnvme_dev_get_geo(xnvme_dev* dev)

    xnvme_spec_idfy_ctrlr* xnvme_dev_get_ctrlr(xnvme_dev* dev)

    xnvme_spec_idfy_ctrlr* xnvme_dev_get_ctrlr_css(xnvme_dev* dev)

    xnvme_spec_idfy_ns* xnvme_dev_get_ns(xnvme_dev* dev)

    xnvme_spec_idfy_ns* xnvme_dev_get_ns_css(xnvme_dev* dev)

    uint32_t xnvme_dev_get_nsid(xnvme_dev* dev)

    uint8_t xnvme_dev_get_csi(xnvme_dev* dev)

    xnvme_ident* xnvme_dev_get_ident(xnvme_dev* dev)

    void* xnvme_dev_get_be_state(xnvme_dev* dev)

    uint64_t xnvme_dev_get_ssw(xnvme_dev* dev)

    void* xnvme_buf_phys_alloc(xnvme_dev* dev, size_t nbytes, uint64_t* phys)

    void xnvme_buf_phys_free(xnvme_dev* dev, void* buf)

    void* xnvme_buf_phys_realloc(xnvme_dev* dev, void* buf, size_t nbytes, uint64_t* phys)

    int xnvme_buf_vtophys(xnvme_dev* dev, void* buf, uint64_t* phys)

    void* xnvme_buf_virt_alloc(size_t alignment, size_t nbytes)

    void xnvme_buf_virt_free(void* buf)

    uint64_t XNVME_ILOG2(uint64_t x)

    int XNVME_MIN(int x, int y)

    uint64_t XNVME_MIN_U64(uint64_t x, uint64_t y)

    int64_t XNVME_MIN_S64(int64_t x, int64_t y)

    int XNVME_MAX(int x, int y)

    uint64_t _xnvme_timer_clock_sample()

    cdef struct xnvme_timer:
        uint64_t start
        uint64_t stop

    uint64_t xnvme_timer_start(xnvme_timer* t)

    uint64_t xnvme_timer_stop(xnvme_timer* t)

    double xnvme_timer_elapsed_secs(xnvme_timer* t)

    double xnvme_timer_elapsed(xnvme_timer* t)

    double xnvme_timer_elapsed_msecs(xnvme_timer* t)

    double xnvme_timer_elapsed_usecs(xnvme_timer* t)

    uint64_t xnvme_timer_elapsed_nsecs(xnvme_timer* t)

    void xnvme_timer_pr(xnvme_timer* t, char* prefix)

    void xnvme_timer_bw_pr(xnvme_timer* t, char* prefix, size_t nbytes)

    int xnvme_is_pow2(uint32_t val)

    cpdef enum xnvme_geo_type:
        XNVME_GEO_UNKNOWN
        XNVME_GEO_CONVENTIONAL
        XNVME_GEO_ZONED

    cdef struct xnvme_geo:
        xnvme_geo_type type
        uint32_t npugrp
        uint32_t npunit
        uint32_t nzone
        uint64_t nsect
        uint32_t nbytes
        uint32_t nbytes_oob
        uint64_t tbytes
        uint64_t ssw
        uint32_t mdts_nbytes
        uint32_t lba_nbytes
        uint8_t lba_extended
        uint8_t _rsvd[7]

    cdef struct xnvme_ident:
        char uri[384]
        uint32_t dtype
        uint32_t nsid
        uint8_t csi
        uint8_t rsvd[3]

    int xnvme_ident_from_uri(char* uri, xnvme_ident* ident)

    cdef struct xnvme_spec_ctrlr_bar:
        uint64_t cap
        uint32_t vs
        uint32_t intms
        uint32_t intmc
        uint32_t cc
        uint32_t rsvd24
        uint32_t csts
        uint32_t nssr
        uint32_t aqa
        uint64_t asq
        uint64_t acq
        uint32_t cmbloc
        uint32_t cmbsz
        uint32_t bpinfo
        uint32_t bprsel
        uint64_t bpmbl
        uint64_t cmbmsc
        uint32_t cmbsts
        uint8_t rsvd92[3492]
        uint32_t pmrcap
        uint32_t pmrctl
        uint32_t pmrsts
        uint32_t pmrebs
        uint32_t pmrswtp
        uint32_t pmrmscl
        uint32_t pmrmscu
        uint8_t css[484]

    cpdef enum xnvme_spec_status_code_type:
        XNVME_STATUS_CODE_TYPE_GENERIC
        XNVME_STATUS_CODE_TYPE_CMDSPEC
        XNVME_STATUS_CODE_TYPE_MEDIA
        XNVME_STATUS_CODE_TYPE_PATH
        XNVME_STATUS_CODE_TYPE_VENDOR

    cdef struct xnvme_spec_status:
        uint16_t val
        uint16_t p
        uint16_t sc
        uint16_t sct
        uint16_t rsvd2
        uint16_t m
        uint16_t dnr

    cdef struct xnvme_spec_cpl:
        uint16_t sqhd
        uint16_t sqid
        uint16_t cid
        xnvme_spec_status status
        uint64_t result
        uint32_t cdw0
        uint32_t rsvd1

    cdef struct xnvme_spec_log_health_entry:
        uint8_t crit_warn
        uint16_t comp_temp
        uint8_t avail_spare
        uint8_t avail_spare_thresh
        uint8_t pct_used
        uint8_t eg_crit_warn_sum
        uint8_t rsvd8[25]
        uint8_t data_units_read[16]
        uint8_t data_units_written[16]
        uint8_t host_read_cmds[16]
        uint8_t host_write_cmds[16]
        uint8_t ctrlr_busy_time[16]
        uint8_t pwr_cycles[16]
        uint8_t pwr_on_hours[16]
        uint8_t unsafe_shutdowns[16]
        uint8_t mdi_errs[16]
        uint8_t nr_err_logs[16]
        uint32_t warn_comp_temp_time
        uint32_t crit_comp_temp_time
        uint16_t temp_sens[8]
        uint32_t tmt1tc
        uint32_t tmt2tc
        uint32_t tttmt1
        uint32_t tttmt2
        uint8_t rsvd[280]

    cdef struct xnvme_spec_log_erri_entry:
        uint64_t ecnt
        uint16_t sqid
        uint16_t cid
        xnvme_spec_status status
        uint16_t eloc
        uint64_t lba
        uint32_t nsid
        uint8_t ven_si
        uint8_t trtype
        uint8_t reserved30[2]
        uint64_t cmd_si
        uint16_t trtype_si
        uint8_t reserved42[22]

    cpdef enum xnvme_spec_log_lpi:
        XNVME_SPEC_LOG_RSVD
        XNVME_SPEC_LOG_ERRI
        XNVME_SPEC_LOG_HEALTH
        XNVME_SPEC_LOG_FW
        XNVME_SPEC_LOG_CHNS
        XNVME_SPEC_LOG_CSAE
        XNVME_SPEC_LOG_SELFTEST
        XNVME_SPEC_LOG_TELEHOST
        XNVME_SPEC_LOG_TELECTRLR

    cpdef enum xnvme_spec_idfy_cns:
        XNVME_SPEC_IDFY_NS
        XNVME_SPEC_IDFY_CTRLR
        XNVME_SPEC_IDFY_NSLIST
        XNVME_SPEC_IDFY_NSDSCR
        XNVME_SPEC_IDFY_SETL
        XNVME_SPEC_IDFY_NS_IOCS
        XNVME_SPEC_IDFY_CTRLR_IOCS
        XNVME_SPEC_IDFY_NSLIST_IOCS
        XNVME_SPEC_IDFY_NSLIST_ALLOC
        XNVME_SPEC_IDFY_NS_ALLOC
        XNVME_SPEC_IDFY_CTRLR_NS
        XNVME_SPEC_IDFY_CTRLR_SUB
        XNVME_SPEC_IDFY_CTRLR_PRI
        XNVME_SPEC_IDFY_CTRLR_SEC
        XNVME_SPEC_IDFY_NSGRAN
        XNVME_SPEC_IDFY_UUIDL
        XNVME_SPEC_IDFY_NSLIST_ALLOC_IOCS
        XNVME_SPEC_IDFY_NS_ALLOC_IOCS
        XNVME_SPEC_IDFY_IOCS

    cdef struct xnvme_spec_lbaf:
        uint16_t ms
        uint8_t ds
        uint8_t rp
        uint8_t rsvd

    cpdef enum xnvme_spec_csi:
        XNVME_SPEC_CSI_NVM
        XNVME_SPEC_CSI_ZONED

    cdef struct xnvme_spec_idfy_ns:
        uint64_t nsze
        uint64_t ncap
        uint64_t nuse
        uint8_t nlbaf
        uint16_t nawun
        uint16_t nawupf
        uint16_t nacwu
        uint16_t nabsn
        uint16_t nabo
        uint16_t nabspf
        uint16_t noiob
        uint64_t nvmcap[2]
        uint8_t reserved64[40]
        uint8_t nguid[16]
        uint64_t eui64
        xnvme_spec_lbaf lbaf[16]
        uint8_t rsvd3776[3648]
        uint8_t vendor_specific[256]
        uint8_t nsfeat__thin_prov "nsfeat.thin_prov"
        uint8_t nsfeat__ns_atomic_write_unit "nsfeat.ns_atomic_write_unit"
        uint8_t nsfeat__dealloc_or_unwritten_error "nsfeat.dealloc_or_unwritten_error"
        uint8_t nsfeat__guid_never_reused "nsfeat.guid_never_reused"
        uint8_t nsfeat__reserved1 "nsfeat.reserved1"
        uint8_t flbas__format "flbas.format"
        uint8_t flbas__extended "flbas.extended"
        uint8_t flbas__reserved2 "flbas.reserved2"
        uint8_t mc__extended "mc.extended"
        uint8_t mc__pointer "mc.pointer"
        uint8_t mc__reserved3 "mc.reserved3"
        uint8_t dpc__val "dpc.val"
        uint8_t dpc__pit1 "dpc.pit1"
        uint8_t dpc__pit2 "dpc.pit2"
        uint8_t dpc__pit3 "dpc.pit3"
        uint8_t dpc__md_start "dpc.md_start"
        uint8_t dpc__md_end "dpc.md_end"
        uint8_t dps__val "dps.val"
        uint8_t dps__pit "dps.pit"
        uint8_t dps__md_start "dps.md_start"
        uint8_t dps__reserved4 "dps.reserved4"
        uint8_t nmic__can_share "nmic.can_share"
        uint8_t nmic__reserved "nmic.reserved"
        uint8_t nsrescap__val "nsrescap.val"
        uint8_t nsrescap__persist "nsrescap.persist"
        uint8_t nsrescap__write_exclusive "nsrescap.write_exclusive"
        uint8_t nsrescap__exclusive_access "nsrescap.exclusive_access"
        uint8_t nsrescap__write_exclusive_reg_only "nsrescap.write_exclusive_reg_only"
        uint8_t nsrescap__exclusive_access_reg_only "nsrescap.exclusive_access_reg_only"
        uint8_t nsrescap__write_exclusive_all_reg "nsrescap.write_exclusive_all_reg"
        uint8_t nsrescap__exclusive_access_all_reg "nsrescap.exclusive_access_all_reg"
        uint8_t nsrescap__ignore_existing_key "nsrescap.ignore_existing_key"
        uint8_t fpi__val "fpi.val"
        uint8_t fpi__percentage_remaining "fpi.percentage_remaining"
        uint8_t fpi__fpi_supported "fpi.fpi_supported"
        uint8_t dlfeat__val "dlfeat.val"
        uint8_t dlfeat__bits__read_value "dlfeat.bits.read_value"
        uint8_t dlfeat__bits__write_zero_deallocate "dlfeat.bits.write_zero_deallocate"
        uint8_t dlfeat__bits__guard_value "dlfeat.bits.guard_value"
        uint8_t dlfeat__bits__reserved "dlfeat.bits.reserved"

    cdef struct xnvme_spec_power_state:
        uint16_t mp
        uint8_t reserved1
        uint8_t mps
        uint8_t nops
        uint8_t reserved2
        uint32_t enlat
        uint32_t exlat
        uint8_t rrt
        uint8_t reserved3
        uint8_t rrl
        uint8_t reserved4
        uint8_t rwt
        uint8_t reserved5
        uint8_t rwl
        uint8_t reserved6
        uint8_t reserved7[16]

    cdef union xnvme_spec_vs_register:
        uint32_t val
        uint32_t bits__ter "bits.ter"
        uint32_t bits__mnr "bits.mnr"
        uint32_t bits__mjr "bits.mjr"

    cdef struct xnvme_spec_idfy_ctrlr:
        uint16_t vid
        uint16_t ssvid
        int8_t sn[20]
        int8_t mn[40]
        uint8_t fr[8]
        uint8_t rab
        uint8_t ieee[3]
        uint8_t mdts
        uint16_t cntlid
        xnvme_spec_vs_register ver
        uint32_t rtd3r
        uint32_t rtd3e
        uint8_t reserved_100[12]
        uint8_t fguid[16]
        uint8_t reserved_128[128]
        uint8_t acl
        uint8_t aerl
        uint8_t elpe
        uint8_t npss
        uint16_t wctemp
        uint16_t cctemp
        uint16_t mtfa
        uint32_t hmpre
        uint32_t hmmin
        uint64_t tnvmcap[2]
        uint64_t unvmcap[2]
        uint16_t edstt
        uint8_t fwug
        uint16_t kas
        uint16_t mntmt
        uint16_t mxtmt
        uint8_t reserved3[180]
        uint16_t maxcmd
        uint32_t nn
        uint16_t fuses
        uint16_t awun
        uint16_t awupf
        uint8_t nvscc
        uint8_t reserved531
        uint16_t acwu
        uint16_t reserved534
        uint32_t mnan
        uint8_t reserved4[224]
        uint8_t subnqn[256]
        uint8_t reserved5[768]
        xnvme_spec_power_state psd[32]
        uint8_t vs[1024]
        uint8_t cmic__val "cmic.val"
        uint8_t cmic__multi_port "cmic.multi_port"
        uint8_t cmic__multi_host "cmic.multi_host"
        uint8_t cmic__sr_iov "cmic.sr_iov"
        uint8_t cmic__reserved "cmic.reserved"
        uint32_t oaes__val "oaes.val"
        uint32_t oaes__reserved1 "oaes.reserved1"
        uint32_t oaes__ns_attribute_notices "oaes.ns_attribute_notices"
        uint32_t oaes__fw_activation_notices "oaes.fw_activation_notices"
        uint32_t oaes__reserved2 "oaes.reserved2"
        uint32_t oaes__zone_changes "oaes.zone_changes"
        uint32_t oaes__reserved3 "oaes.reserved3"
        uint32_t ctratt__val "ctratt.val"
        uint32_t ctratt__host_id_exhid_supported "ctratt.host_id_exhid_supported"
        uint32_t ctratt__non_operational_power_state_permissive_mode "ctratt.non_operational_power_state_permissive_mode"
        uint32_t ctratt__reserved "ctratt.reserved"
        uint16_t oacs__val "oacs.val"
        uint16_t oacs__security "oacs.security"
        uint16_t oacs__format "oacs.format"
        uint16_t oacs__firmware "oacs.firmware"
        uint16_t oacs__ns_manage "oacs.ns_manage"
        uint16_t oacs__device_self_test "oacs.device_self_test"
        uint16_t oacs__directives "oacs.directives"
        uint16_t oacs__nvme_mi "oacs.nvme_mi"
        uint16_t oacs__virtualization_management "oacs.virtualization_management"
        uint16_t oacs__doorbell_buffer_config "oacs.doorbell_buffer_config"
        uint16_t oacs__oacs_rsvd "oacs.oacs_rsvd"
        uint8_t frmw__val "frmw.val"
        uint8_t frmw__slot1_ro "frmw.slot1_ro"
        uint8_t frmw__num_slots "frmw.num_slots"
        uint8_t frmw__activation_without_reset "frmw.activation_without_reset"
        uint8_t frmw__frmw_rsvd "frmw.frmw_rsvd"
        uint8_t lpa__val "lpa.val"
        uint8_t lpa__ns_smart "lpa.ns_smart"
        uint8_t lpa__celp "lpa.celp"
        uint8_t lpa__edlp "lpa.edlp"
        uint8_t lpa__telemetry "lpa.telemetry"
        uint8_t lpa__pel "lpa.pel"
        uint8_t lpa__lpa_rsvd "lpa.lpa_rsvd"
        uint8_t avscc__val "avscc.val"
        uint8_t avscc__spec_format "avscc.spec_format"
        uint8_t avscc__avscc_rsvd "avscc.avscc_rsvd"
        uint8_t apsta__val "apsta.val"
        uint8_t apsta__supported "apsta.supported"
        uint8_t apsta__apsta_rsvd "apsta.apsta_rsvd"
        uint32_t rpmbs__val "rpmbs.val"
        uint8_t rpmbs__num_rpmb_units "rpmbs.num_rpmb_units"
        uint8_t rpmbs__auth_method "rpmbs.auth_method"
        uint8_t rpmbs__reserved1 "rpmbs.reserved1"
        uint8_t rpmbs__reserved2 "rpmbs.reserved2"
        uint8_t rpmbs__total_size "rpmbs.total_size"
        uint8_t rpmbs__access_size "rpmbs.access_size"
        uint8_t dsto__val "dsto.val"
        uint8_t dsto__bits__one_only "dsto.bits.one_only"
        uint8_t dsto__bits__reserved "dsto.bits.reserved"
        uint16_t hctma__val "hctma.val"
        uint16_t hctma__bits__supported "hctma.bits.supported"
        uint16_t hctma__bits__reserved "hctma.bits.reserved"
        uint32_t sanicap__val "sanicap.val"
        uint32_t sanicap__bits__crypto_erase "sanicap.bits.crypto_erase"
        uint32_t sanicap__bits__block_erase "sanicap.bits.block_erase"
        uint32_t sanicap__bits__overwrite "sanicap.bits.overwrite"
        uint32_t sanicap__bits__reserved "sanicap.bits.reserved"
        uint8_t sqes__val "sqes.val"
        uint8_t sqes__min "sqes.min"
        uint8_t sqes__max "sqes.max"
        uint8_t cqes__val "cqes.val"
        uint8_t cqes__min "cqes.min"
        uint8_t cqes__max "cqes.max"
        uint16_t oncs__val "oncs.val"
        uint16_t oncs__compare "oncs.compare"
        uint16_t oncs__write_unc "oncs.write_unc"
        uint16_t oncs__dsm "oncs.dsm"
        uint16_t oncs__write_zeroes "oncs.write_zeroes"
        uint16_t oncs__set_features_save "oncs.set_features_save"
        uint16_t oncs__reservations "oncs.reservations"
        uint16_t oncs__timestamp "oncs.timestamp"
        uint16_t oncs__reserved "oncs.reserved"
        uint8_t fna__val "fna.val"
        uint8_t fna__format_all_ns "fna.format_all_ns"
        uint8_t fna__erase_all_ns "fna.erase_all_ns"
        uint8_t fna__crypto_erase_supported "fna.crypto_erase_supported"
        uint8_t fna__reserved "fna.reserved"
        uint8_t vwc__val "vwc.val"
        uint8_t vwc__present "vwc.present"
        uint8_t vwc__flush_broadcast "vwc.flush_broadcast"
        uint8_t vwc__reserved "vwc.reserved"
        uint32_t sgls__val "sgls.val"
        uint32_t sgls__supported "sgls.supported"
        uint32_t sgls__keyed_sgl "sgls.keyed_sgl"
        uint32_t sgls__reserved1 "sgls.reserved1"
        uint32_t sgls__bit_bucket_descriptor "sgls.bit_bucket_descriptor"
        uint32_t sgls__metadata_pointer "sgls.metadata_pointer"
        uint32_t sgls__oversized_sgl "sgls.oversized_sgl"
        uint32_t sgls__metadata_address "sgls.metadata_address"
        uint32_t sgls__sgl_offset "sgls.sgl_offset"
        uint32_t sgls__transport_sgl "sgls.transport_sgl"
        uint32_t sgls__reserved2 "sgls.reserved2"
        uint32_t nvmf_specific__ioccsz "nvmf_specific.ioccsz"
        uint32_t nvmf_specific__iorcsz "nvmf_specific.iorcsz"
        uint16_t nvmf_specific__icdoff "nvmf_specific.icdoff"
        uint8_t nvmf_specific__msdbd "nvmf_specific.msdbd"
        uint8_t nvmf_specific__reserved "nvmf_specific.reserved[244]"
        uint8_t nvmf_specific__ctrattr__ctrlr_model "nvmf_specific.ctrattr.ctrlr_model"
        uint8_t nvmf_specific__ctrattr__reserved "nvmf_specific.ctrattr.reserved"

    cdef struct xnvme_spec_cs_vector:
        uint64_t val
        uint64_t nvm
        uint64_t rsvd1
        uint64_t zns
        uint64_t rsvd

    cdef struct xnvme_spec_idfy_cs:
        xnvme_spec_cs_vector iocsc[512]

    cdef struct xnvme_spec_idfy:
        xnvme_spec_idfy_ctrlr ctrlr
        xnvme_spec_idfy_ns ns
        xnvme_spec_idfy_cs cs

    cpdef enum xnvme_spec_adm_opc:
        XNVME_SPEC_ADM_OPC_LOG
        XNVME_SPEC_ADM_OPC_IDFY
        XNVME_SPEC_ADM_OPC_SFEAT
        XNVME_SPEC_ADM_OPC_GFEAT

    cpdef enum xnvme_spec_nvm_opc:
        XNVME_SPEC_NVM_OPC_FLUSH
        XNVME_SPEC_NVM_OPC_WRITE
        XNVME_SPEC_NVM_OPC_READ
        XNVME_SPEC_NVM_OPC_WRITE_UNCORRECTABLE
        XNVME_SPEC_NVM_OPC_WRITE_ZEROES
        XNVME_SPEC_NVM_OPC_SCOPY
        XNVME_SPEC_NVM_OPC_FMT
        XNVME_SPEC_NVM_OPC_SANITIZE

    cpdef enum xnvme_spec_feat_id:
        XNVME_SPEC_FEAT_ARBITRATION
        XNVME_SPEC_FEAT_PWR_MGMT
        XNVME_SPEC_FEAT_LBA_RANGETYPE
        XNVME_SPEC_FEAT_TEMP_THRESHOLD
        XNVME_SPEC_FEAT_ERROR_RECOVERY
        XNVME_SPEC_FEAT_VWCACHE
        XNVME_SPEC_FEAT_NQUEUES

    cpdef enum xnvme_spec_feat_sel:
        XNVME_SPEC_FEAT_SEL_CURRENT
        XNVME_SPEC_FEAT_SEL_DEFAULT
        XNVME_SPEC_FEAT_SEL_SAVED
        XNVME_SPEC_FEAT_SEL_SUPPORTED

    cdef struct xnvme_spec_feat:
        uint32_t val
        uint32_t temp_threshold__tmpth "temp_threshold.tmpth"
        uint32_t temp_threshold__tmpsel "temp_threshold.tmpsel"
        uint32_t temp_threshold__thsel "temp_threshold.thsel"
        uint32_t error_recovery__tler "error_recovery.tler"
        uint32_t error_recovery__dulbe "error_recovery.dulbe"
        uint32_t error_recovery__rsvd "error_recovery.rsvd"
        uint32_t nqueues__nsqa "nqueues.nsqa"
        uint32_t nqueues__ncqa "nqueues.ncqa"

    cdef struct xnvme_spec_dsm_range:
        uint32_t cattr
        uint32_t nlb
        uint64_t slba

    cpdef enum xnvme_spec_flag:
        XNVME_SPEC_FLAG_LIMITED_RETRY
        XNVME_SPEC_FLAG_FORCE_UNIT_ACCESS
        XNVME_SPEC_FLAG_PRINFO_PRCHK_REF
        XNVME_SPEC_FLAG_PRINFO_PRCHK_APP
        XNVME_SPEC_FLAG_PRINFO_PRCHK_GUARD
        XNVME_SPEC_FLAG_PRINFO_PRACT

    cpdef enum xnvme_nvme_sgl_descriptor_type:
        XNVME_SPEC_SGL_DESCR_TYPE_DATA_BLOCK
        XNVME_SPEC_SGL_DESCR_TYPE_BIT_BUCKET
        XNVME_SPEC_SGL_DESCR_TYPE_SEGMENT
        XNVME_SPEC_SGL_DESCR_TYPE_LAST_SEGMENT
        XNVME_SPEC_SGL_DESCR_TYPE_KEYED_DATA_BLOCK
        XNVME_SPEC_SGL_DESCR_TYPE_VENDOR_SPECIFIC

    cpdef enum xnvme_spec_sgl_descriptor_subtype:
        XNVME_SPEC_SGL_DESCR_SUBTYPE_ADDRESS
        XNVME_SPEC_SGL_DESCR_SUBTYPE_OFFSET

    cdef struct xnvme_spec_sgl_descriptor:
        uint64_t addr
        uint64_t generic__rsvd "generic.rsvd"
        uint64_t generic__subtype "generic.subtype"
        uint64_t generic__type "generic.type"
        uint64_t unkeyed__len "unkeyed.len"
        uint64_t unkeyed__rsvd "unkeyed.rsvd"
        uint64_t unkeyed__subtype "unkeyed.subtype"
        uint64_t unkeyed__type "unkeyed.type"

    cpdef enum xnvme_spec_psdt:
        XNVME_SPEC_PSDT_PRP
        XNVME_SPEC_PSDT_SGL_MPTR_CONTIGUOUS
        XNVME_SPEC_PSDT_SGL_MPTR_SGL

    cdef struct xnvme_spec_cmd_common:
        uint16_t opcode
        uint16_t fuse
        uint16_t rsvd
        uint16_t psdt
        uint16_t cid
        uint32_t nsid
        uint32_t cdw02
        uint32_t cdw03
        uint64_t mptr
        uint32_t ndt
        uint32_t ndm
        uint32_t cdw12
        uint32_t cdw13
        uint32_t cdw14
        uint32_t cdw15
        xnvme_spec_sgl_descriptor dptr__sgl "dptr.sgl"
        uint64_t dptr__prp__prp1 "dptr.prp.prp1"
        uint64_t dptr__prp__prp2 "dptr.prp.prp2"
        uint64_t dptr__lnx_ioctl__data "dptr.lnx_ioctl.data"
        uint32_t dptr__lnx_ioctl__metadata_len "dptr.lnx_ioctl.metadata_len"
        uint32_t dptr__lnx_ioctl__data_len "dptr.lnx_ioctl.data_len"

    cdef struct xnvme_spec_cmd_sanitize:
        uint32_t cdw00_09[10]
        uint32_t sanact
        uint32_t ause
        uint32_t owpass
        uint32_t oipbp
        uint32_t nodas
        uint32_t rsvd
        uint32_t ovrpat
        uint32_t cdw12_15[4]

    cdef struct xnvme_spec_cmd_format:
        uint32_t cdw00_09[10]
        uint32_t lbaf
        uint32_t mset
        uint32_t pi
        uint32_t pil
        uint32_t ses
        uint32_t zf
        uint32_t rsvd
        uint32_t cdw11_15[5]

    cdef struct xnvme_spec_cmd_gfeat:
        uint32_t cdw00_09[10]
        uint32_t cdw11_15[5]
        uint32_t cdw10__val "cdw10.val"
        uint32_t cdw10__fid "cdw10.fid"
        uint32_t cdw10__sel "cdw10.sel"
        uint32_t cdw10__rsvd10 "cdw10.rsvd10"

    cdef struct xnvme_spec_cmd_sfeat:
        uint32_t cdw00_09[10]
        xnvme_spec_feat feat
        uint32_t cdw12_15[4]
        uint32_t cdw10__val "cdw10.val"
        uint32_t cdw10__fid "cdw10.fid"
        uint32_t cdw10__rsvd10 "cdw10.rsvd10"
        uint32_t cdw10__save "cdw10.save"

    cdef struct xnvme_spec_cmd_idfy:
        uint32_t cdw00_09[10]
        uint32_t cns
        uint32_t rsvd1
        uint32_t cntid
        uint32_t nvmsetid
        uint32_t rsvd2
        uint32_t csi
        uint32_t cdw12_13[2]
        uint32_t uuid
        uint32_t rsvd3
        uint32_t cdw15

    cdef struct xnvme_spec_cmd_log:
        uint32_t cdw00_09[10]
        uint32_t lid
        uint32_t lsp
        uint32_t rsvd10
        uint32_t rae
        uint32_t numdl
        uint32_t numdu
        uint32_t rsvd11
        uint32_t lpol
        uint32_t lpou
        uint32_t cdw14_15[2]

    cdef struct xnvme_spec_cmd_nvm:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd
        uint32_t dtype
        uint32_t rsvd2
        uint32_t prinfo
        uint32_t fua
        uint32_t lr
        uint32_t cdw13_15[3]

    cdef struct xnvme_spec_nvm_write_zeroes:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd1
        uint32_t deac
        uint32_t prinfo
        uint32_t fua
        uint32_t lr
        uint32_t cdw_13
        uint32_t ilbrt
        uint32_t lbat
        uint32_t lbatm

    cpdef enum xnvme_spec_nvm_cmd_cpl_sc:
        XNVME_SPEC_NVM_CMD_CPL_SC_WRITE_TO_RONLY

    cdef struct xnvme_spec_nvm_scopy_fmt_zero:
        uint8_t rsvd0[8]
        uint64_t slba
        uint32_t nlb
        uint32_t rsvd20
        uint32_t eilbrt
        uint32_t elbatm
        uint32_t elbat

    cpdef enum xnvme_nvm_scopy_fmt:
        XNVME_NVM_SCOPY_FMT_ZERO
        XNVME_NVM_SCOPY_FMT_SRCLEN

    cdef struct xnvme_spec_nvm_scopy_source_range:
        xnvme_spec_nvm_scopy_fmt_zero entry[128]

    cdef struct xnvme_spec_nvm_cmd_scopy:
        uint32_t cdw00_09[10]
        uint64_t sdlba
        uint32_t nr
        uint32_t df
        uint32_t prinfor
        uint32_t rsvd1
        uint32_t dtype
        uint32_t rsvd2
        uint32_t prinfow
        uint32_t fua
        uint32_t lr
        uint32_t rsvd3
        uint32_t dspec
        uint32_t ilbrt
        uint32_t lbat
        uint32_t lbatm

    cdef struct xnvme_spec_nvm_cmd_scopy_fmt_srclen:
        uint64_t start
        uint64_t len

    cdef struct xnvme_spec_nvm_cmd:
        xnvme_spec_nvm_cmd_scopy scopy

    cdef struct xnvme_spec_nvm_idfy_ctrlr:
        uint8_t byte0_519[520]
        uint8_t byte522_533[12]
        uint8_t byte536_4095[3559]
        uint16_t oncs__val "oncs.val"
        uint16_t oncs__compare "oncs.compare"
        uint16_t oncs__write_unc "oncs.write_unc"
        uint16_t oncs__dsm "oncs.dsm"
        uint16_t oncs__write_zeroes "oncs.write_zeroes"
        uint16_t oncs__set_features_save "oncs.set_features_save"
        uint16_t oncs__reservations "oncs.reservations"
        uint16_t oncs__timestamp "oncs.timestamp"
        uint16_t oncs__verify "oncs.verify"
        uint16_t oncs__copy "oncs.copy"
        uint16_t oncs__reserved "oncs.reserved"
        uint16_t ocfs__val "ocfs.val"
        uint16_t ocfs__copy_fmt0 "ocfs.copy_fmt0"
        uint16_t ocfs__rsvd "ocfs.rsvd"

    cdef struct xnvme_spec_nvm_idfy_ns:
        uint8_t byte0_73[74]
        uint16_t mssrl
        uint32_t mcl
        uint8_t msrc
        uint8_t byte81_4095[4014]

    cdef struct xnvme_spec_nvm_idfy:
        xnvme_spec_idfy base
        xnvme_spec_nvm_idfy_ctrlr ctrlr
        xnvme_spec_nvm_idfy_ns ns

    cpdef enum xnvme_spec_znd_log_lid:
        XNVME_SPEC_LOG_ZND_CHANGES

    cpdef enum xnvme_spec_znd_opc:
        XNVME_SPEC_ZND_OPC_MGMT_SEND
        XNVME_SPEC_ZND_OPC_MGMT_RECV
        XNVME_SPEC_ZND_OPC_APPEND

    cdef struct xnvme_spec_znd_cmd_mgmt_send:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t nrange
        uint32_t zsa
        uint32_t select_all
        uint32_t zsaso
        uint32_t rsvd
        uint32_t cdw14_15[2]

    cdef struct xnvme_spec_znd_cmd_mgmt_recv:
        uint32_t cdw00_09[10]
        uint64_t slba
        uint32_t ndwords
        uint32_t zra
        uint32_t zrasf
        uint32_t partial
        uint32_t rsvd
        uint64_t addrs_dst

    cdef struct xnvme_spec_znd_cmd_append:
        uint32_t cdw00_09[10]
        uint64_t zslba
        uint32_t nlb
        uint32_t rsvd
        uint32_t dtype
        uint32_t prinfo
        uint32_t rsvd2
        uint32_t fua
        uint32_t lr
        uint32_t cdw13_15[3]

    cdef struct xnvme_spec_znd_cmd:
        xnvme_spec_znd_cmd_mgmt_send mgmt_send
        xnvme_spec_znd_cmd_mgmt_recv mgmt_recv
        xnvme_spec_znd_cmd_append append

    cdef struct xnvme_spec_cmd:
        xnvme_spec_cmd_common common
        xnvme_spec_cmd_sanitize sanitize
        xnvme_spec_cmd_format format
        xnvme_spec_cmd_log log
        xnvme_spec_cmd_gfeat gfeat
        xnvme_spec_cmd_sfeat sfeat
        xnvme_spec_cmd_idfy idfy
        xnvme_spec_cmd_nvm nvm
        xnvme_spec_nvm_cmd_scopy scopy
        xnvme_spec_nvm_write_zeroes write_zeroes
        xnvme_spec_znd_cmd znd

    cpdef enum xnvme_spec_znd_status_code:
        XNVME_SPEC_ZND_SC_INVALID_FORMAT
        XNVME_SPEC_ZND_SC_INVALID_ZONE_OP
        XNVME_SPEC_ZND_SC_NOZRWA
        XNVME_SPEC_ZND_SC_BOUNDARY_ERROR
        XNVME_SPEC_ZND_SC_IS_FULL
        XNVME_SPEC_ZND_SC_IS_READONLY
        XNVME_SPEC_ZND_SC_IS_OFFLINE
        XNVME_SPEC_ZND_SC_INVALID_WRITE
        XNVME_SPEC_ZND_SC_TOO_MANY_ACTIVE
        XNVME_SPEC_ZND_SC_TOO_MANY_OPEN
        XNVME_SPEC_ZND_SC_INVALID_TRANS

    cpdef enum xnvme_spec_znd_mgmt_send_action_so:
        XNVME_SPEC_ZND_MGMT_OPEN_WITH_ZRWA

    cpdef enum xnvme_spec_znd_cmd_mgmt_send_action:
        XNVME_SPEC_ZND_CMD_MGMT_SEND_CLOSE
        XNVME_SPEC_ZND_CMD_MGMT_SEND_FINISH
        XNVME_SPEC_ZND_CMD_MGMT_SEND_OPEN
        XNVME_SPEC_ZND_CMD_MGMT_SEND_RESET
        XNVME_SPEC_ZND_CMD_MGMT_SEND_OFFLINE
        XNVME_SPEC_ZND_CMD_MGMT_SEND_DESCRIPTOR
        XNVME_SPEC_ZND_CMD_MGMT_SEND_FLUSH

    cpdef enum xnvme_spec_znd_cmd_mgmt_recv_action_sf:
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_ALL
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_EMPTY
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_IOPEN
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_EOPEN
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_CLOSED
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_FULL
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_RONLY
        XNVME_SPEC_ZND_CMD_MGMT_RECV_SF_OFFLINE

    cpdef enum xnvme_spec_znd_cmd_mgmt_recv_action:
        XNVME_SPEC_ZND_CMD_MGMT_RECV_ACTION_REPORT
        XNVME_SPEC_ZND_CMD_MGMT_RECV_ACTION_REPORT_EXTENDED

    cpdef enum xnvme_spec_znd_type:
        XNVME_SPEC_ZND_TYPE_SEQWR

    cpdef enum xnvme_spec_znd_state:
        XNVME_SPEC_ZND_STATE_EMPTY
        XNVME_SPEC_ZND_STATE_IOPEN
        XNVME_SPEC_ZND_STATE_EOPEN
        XNVME_SPEC_ZND_STATE_CLOSED
        XNVME_SPEC_ZND_STATE_RONLY
        XNVME_SPEC_ZND_STATE_FULL
        XNVME_SPEC_ZND_STATE_OFFLINE

    cdef struct xnvme_spec_znd_idfy_ctrlr:
        uint8_t zasl
        uint8_t rsvd8[4095]

    cdef struct xnvme_spec_znd_idfy_lbafe:
        uint64_t zsze
        uint8_t zdes
        uint8_t rsvd[7]

    cdef struct xnvme_spec_znd_idfy_ns:
        uint32_t mar
        uint32_t mor
        uint32_t rrl
        uint32_t frl
        uint8_t rsvd12[24]
        uint32_t numzrwa
        uint16_t zrwafg
        uint16_t zrwas
        uint8_t rsvd53[2763]
        xnvme_spec_znd_idfy_lbafe lbafe[16]
        uint8_t rsvd3072[768]
        uint8_t vs[256]
        uint16_t zoc__val "zoc.val"
        uint16_t zoc__bits__vzcap "zoc.bits.vzcap"
        uint16_t zoc__bits__zae "zoc.bits.zae"
        uint16_t zoc__bits__rsvd "zoc.bits.rsvd"
        uint16_t ozcs__val "ozcs.val"
        uint16_t ozcs__bits__razb "ozcs.bits.razb"
        uint16_t ozcs__bits__zrwasup "ozcs.bits.zrwasup"
        uint16_t ozcs__bits__rsvd "ozcs.bits.rsvd"
        uint8_t zrwacap__val "zrwacap.val"
        uint8_t zrwacap__bits__expflushsup "zrwacap.bits.expflushsup"
        uint8_t zrwacap__bits__rsvd0 "zrwacap.bits.rsvd0"

    cdef struct xnvme_spec_znd_idfy:
        xnvme_spec_idfy base
        xnvme_spec_znd_idfy_ctrlr zctrlr
        xnvme_spec_znd_idfy_ns zns

    cdef struct xnvme_spec_znd_log_changes:
        uint16_t nidents
        uint8_t rsvd2[6]
        uint64_t idents[511]

    cdef struct xnvme_spec_znd_descr:
        uint8_t zt
        uint8_t rsvd0
        uint8_t rsvd1
        uint8_t zs
        uint8_t rsvd7[5]
        uint64_t zcap
        uint64_t zslba
        uint64_t wp
        uint8_t rsvd63[32]
        uint8_t za__val "za.val"
        uint8_t za__zfc "za.zfc"
        uint8_t za__zfr "za.zfr"
        uint8_t za__rzr "za.rzr"
        uint8_t za__zrwav "za.zrwav"
        uint8_t za__rsvd3 "za.rsvd3"
        uint8_t za__zdev "za.zdev"

    cdef struct xnvme_spec_znd_report_hdr:
        uint64_t nzones
        uint8_t rsvd[56]

    int xnvme_spec_log_health_fpr(void* stream, xnvme_spec_log_health_entry* log, int opts)

    int xnvme_spec_log_health_pr(xnvme_spec_log_health_entry* log, int opts)

    int xnvme_spec_log_erri_fpr(void* stream, xnvme_spec_log_erri_entry* log, int limit, int opts)

    int xnvme_spec_log_erri_pr(xnvme_spec_log_erri_entry* log, int limit, int opts)

    int xnvme_spec_idfy_ns_fpr(void* stream, xnvme_spec_idfy_ns* idfy, int opts)

    int xnvme_spec_idfy_ns_pr(xnvme_spec_idfy_ns* idfy, int opts)

    int xnvme_spec_idfy_ctrl_fpr(void* stream, xnvme_spec_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_idfy_ctrl_pr(xnvme_spec_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_idfy_cs_fpr(void* stream, xnvme_spec_idfy_cs* idfy, int opts)

    int xnvme_spec_idfy_cs_pr(xnvme_spec_idfy_cs* idfy, int opts)

    int xnvme_spec_feat_fpr(void* stream, uint8_t fid, xnvme_spec_feat feat, int opts)

    int xnvme_spec_feat_pr(uint8_t fid, xnvme_spec_feat feat, int opts)

    int xnvme_spec_cmd_fpr(void* stream, xnvme_spec_cmd* cmd, int opts)

    int xnvme_spec_cmd_pr(xnvme_spec_cmd* cmd, int opts)

    int xnvme_spec_nvm_scopy_fmt_zero_fpr(void* stream, xnvme_spec_nvm_scopy_fmt_zero* entry, int opts)

    int xnvme_spec_nvm_scopy_fmt_zero_pr(xnvme_spec_nvm_scopy_fmt_zero* entry, int opts)

    int xnvme_spec_nvm_scopy_source_range_fpr(void* stream, xnvme_spec_nvm_scopy_source_range* srange, uint8_t nr, int opts)

    int xnvme_spec_nvm_scopy_source_range_pr(xnvme_spec_nvm_scopy_source_range* srange, uint8_t nr, int opts)

    int xnvme_spec_idfy_ctrlr_fpr(void* stream, xnvme_spec_nvm_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_nvm_idfy_ctrlr_pr(xnvme_spec_nvm_idfy_ctrlr* idfy, int opts)

    int xnvme_spec_nvm_idfy_ns_fpr(void* stream, xnvme_spec_nvm_idfy_ns* idfy, int opts)

    int xnvme_spec_nvm_idfy_ns_pr(xnvme_spec_nvm_idfy_ns* idfy, int opts)

    int xnvme_spec_znd_idfy_ctrlr_fpr(void* stream, xnvme_spec_znd_idfy_ctrlr* zctrlr, int opts)

    int xnvme_spec_znd_idfy_ctrlr_pr(xnvme_spec_znd_idfy_ctrlr* zctrlr, int opts)

    int xnvme_spec_znd_idfy_lbafe_fpr(void* stream, xnvme_spec_znd_idfy_lbafe* zonef, int opts)

    int xnvme_spec_znd_idfy_ns_fpr(void* stream, xnvme_spec_znd_idfy_ns* zns, int opts)

    int xnvme_spec_znd_idfy_ns_pr(xnvme_spec_znd_idfy_ns* zns, int opts)

    int xnvme_spec_znd_log_changes_fpr(void* stream, xnvme_spec_znd_log_changes* changes, int opts)

    int xnvme_spec_znd_log_changes_pr(xnvme_spec_znd_log_changes* changes, int opts)

    int xnvme_spec_znd_descr_fpr(void* stream, xnvme_spec_znd_descr* descr, int opts)

    int xnvme_spec_znd_descr_pr(xnvme_spec_znd_descr* descr, int opts)

    int xnvme_spec_znd_report_hdr_fpr(void* stream, xnvme_spec_znd_report_hdr* hdr, int opts)

    int xnvme_spec_znd_report_hdr_pr(xnvme_spec_znd_report_hdr* hdr, int opts)

    int xnvme_spec_znd_descr_fpr_yaml(void* stream, xnvme_spec_znd_descr* descr, int indent, char* sep)

    cdef struct xnvme_opts:
        char* be
        char* dev
        char* mem
        char* sync
        char* async_ "async"
        char* admin
        uint32_t nsid
        uint32_t create_mode
        uint8_t poll_io
        uint8_t poll_sq
        uint8_t register_files
        uint8_t register_buffers
        uint32_t use_cmb_sqs
        uint32_t shm_id
        uint32_t main_core
        char* core_mask
        char* adrfam
        uint32_t spdk_fabrics
        uint32_t oflags
        uint32_t rdonly
        uint32_t wronly
        uint32_t rdwr
        uint32_t create
        uint32_t truncate
        uint32_t direct
        uint32_t _rsvd
        uint32_t css__value "css.value"
        uint32_t css__given "css.given"

    xnvme_opts xnvme_opts_default()

    cdef struct xnvme_dev

    cpdef enum xnvme_enumerate_action:
        XNVME_ENUMERATE_DEV_KEEP_OPEN
        XNVME_ENUMERATE_DEV_CLOSE

    ctypedef int (*xnvme_enumerate_cb)(xnvme_dev* dev, void* cb_args)

    int xnvme_enumerate(char* sys_uri, xnvme_opts* opts, xnvme_enumerate_cb cb_func, void* cb_args)

    xnvme_dev* xnvme_dev_open(char* dev_uri, xnvme_opts* opts)

    void xnvme_dev_close(xnvme_dev* dev)

    void* xnvme_buf_alloc(xnvme_dev* dev, size_t nbytes)

    void* xnvme_buf_realloc(xnvme_dev* dev, void* buf, size_t nbytes)

    void xnvme_buf_free(xnvme_dev* dev, void* buf)

    cdef struct xnvme_queue

    cpdef enum xnvme_queue_opts:
        XNVME_QUEUE_IOPOLL
        XNVME_QUEUE_SQPOLL

    int xnvme_queue_init(xnvme_dev* dev, uint16_t capacity, int opts, xnvme_queue** queue)

    uint32_t xnvme_queue_get_capacity(xnvme_queue* queue)

    uint32_t xnvme_queue_get_outstanding(xnvme_queue* queue)

    int xnvme_queue_term(xnvme_queue* queue)

    int xnvme_queue_poke(xnvme_queue* queue, uint32_t max)

    int xnvme_queue_drain(xnvme_queue* queue)

    int xnvme_queue_wait(xnvme_queue* queue)

    xnvme_cmd_ctx* xnvme_queue_get_cmd_ctx(xnvme_queue* queue)

    int xnvme_queue_put_cmd_ctx(xnvme_queue* queue, xnvme_cmd_ctx* ctx)

    ctypedef void (*xnvme_queue_cb)(xnvme_cmd_ctx* ctx, void* opaque)

    cdef struct xnvme_cmd_ctx:
        xnvme_spec_cmd cmd
        xnvme_spec_cpl cpl
        xnvme_dev* dev
        uint32_t opts
        uint8_t be_rsvd[4]
        xnvme_queue* async__queue "async.queue"
        xnvme_queue_cb async__cb "async.cb"
        void* async__cb_arg "async.cb_arg"
        xnvme_cmd_ctx* link__sle_next "link.sle_next"

    void xnvme_cmd_ctx_set_cb(xnvme_cmd_ctx* ctx, xnvme_queue_cb cb, void* cb_arg)

    int xnvme_queue_set_cb(xnvme_queue* queue, xnvme_queue_cb cb, void* cb_arg)

    xnvme_cmd_ctx xnvme_cmd_ctx_from_dev(xnvme_dev* dev)

    xnvme_cmd_ctx* xnvme_cmd_ctx_from_queue(xnvme_queue* queue)

    void xnvme_cmd_ctx_clear(xnvme_cmd_ctx* ctx)

    int xnvme_cmd_ctx_cpl_status(xnvme_cmd_ctx* ctx)

    int xnvme_cmd_pass(xnvme_cmd_ctx* ctx, void* dbuf, size_t dbuf_nbytes, void* mbuf, size_t mbuf_nbytes)

    int xnvme_cmd_passv(xnvme_cmd_ctx* ctx, void* dvec, size_t dvec_cnt, size_t dvec_nbytes, void* mvec, size_t mvec_cnt, size_t mvec_nbytes)

    int xnvme_cmd_pass_admin(xnvme_cmd_ctx* ctx, void* dbuf, size_t dbuf_nbytes, void* mbuf, size_t mbuf_nbytes)

    int xnvme_ver_major()

    int xnvme_ver_minor()

    int xnvme_ver_patch()

    int xnvme_ver_fpr(void* stream, int opts)

    int xnvme_ver_pr(int opts)

    int xnvmec_buf_fill(void* buf, size_t nbytes, char* content)

    void* xnvmec_buf_clear(void* buf, size_t nbytes)

    size_t xnvmec_buf_diff(void* expected, void* actual, size_t nbytes)

    void xnvmec_buf_diff_pr(void* expected, void* actual, size_t nbytes, int opts)

    int xnvmec_buf_to_file(void* buf, size_t nbytes, char* path)

    int xnvmec_buf_from_file(void* buf, size_t nbytes, char* path)

    int xnvmec_cmd_from_file(xnvme_spec_cmd* cmd, char* fpath)

    int xnvmec_cmd_to_file(xnvme_spec_cmd* cmd, char* fpath)

    cdef struct xnvmec_args:
        xnvme_dev* dev
        xnvme_geo* geo
        char* uri
        char* sys_uri
        char* cmd_input
        char* cmd_output
        size_t data_nbytes
        char* data_input
        char* data_output
        size_t meta_nbytes
        char* meta_input
        char* meta_output
        uint32_t cdw[16]
        uint64_t lbaf
        uint64_t lba
        uint32_t nlb
        uint64_t slba
        uint64_t elba
        uint32_t uuid
        uint32_t nsid
        uint32_t dev_nsid
        uint32_t cns
        uint32_t csi
        uint64_t index
        uint32_t setid
        uint64_t cntid
        uint32_t lid
        uint32_t lsp
        uint64_t lpo_nbytes
        uint32_t rae
        uint32_t clear
        uint32_t zf
        uint32_t ses
        uint32_t sel
        uint32_t mset
        uint32_t ause
        uint32_t ovrpat
        uint32_t owpass
        uint32_t oipbp
        uint32_t nodas
        uint32_t action
        uint32_t zrms
        uint32_t pi
        uint32_t pil
        uint32_t fid
        uint32_t feat
        uint32_t seed
        uint32_t iosize
        uint32_t qdepth
        uint32_t direct
        uint32_t limit
        uint64_t count
        uint64_t offset
        uint64_t opcode
        uint64_t flags
        uint64_t all
        uint32_t status
        uint32_t save
        uint32_t reset
        uint32_t verbose
        uint32_t help
        char* be
        char* mem
        char* sync
        char* async_ "async"
        char* admin
        uint64_t shm_id
        uint32_t main_core
        char* core_mask
        uint32_t use_cmb_sqs
        char* adrfam
        uint32_t poll_io
        uint32_t poll_sq
        uint32_t register_files
        uint32_t register_buffers
        uint32_t truncate
        uint32_t rdonly
        uint32_t wronly
        uint32_t rdwr
        uint32_t create
        uint32_t create_mode
        uint32_t oflags
        uint32_t vec_cnt
        uint32_t css__value "css.value"
        uint32_t css__given "css.given"

    void xnvmec_args_pr(xnvmec_args* args, int opts)

    cpdef enum xnvmec_opt:
        XNVMEC_OPT_NONE
        XNVMEC_OPT_CDW00
        XNVMEC_OPT_CDW01
        XNVMEC_OPT_CDW02
        XNVMEC_OPT_CDW03
        XNVMEC_OPT_CDW04
        XNVMEC_OPT_CDW05
        XNVMEC_OPT_CDW06
        XNVMEC_OPT_CDW07
        XNVMEC_OPT_CDW08
        XNVMEC_OPT_CDW09
        XNVMEC_OPT_CDW10
        XNVMEC_OPT_CDW11
        XNVMEC_OPT_CDW12
        XNVMEC_OPT_CDW13
        XNVMEC_OPT_CDW14
        XNVMEC_OPT_CDW15
        XNVMEC_OPT_CMD_INPUT
        XNVMEC_OPT_CMD_OUTPUT
        XNVMEC_OPT_DATA_NBYTES
        XNVMEC_OPT_DATA_INPUT
        XNVMEC_OPT_DATA_OUTPUT
        XNVMEC_OPT_META_NBYTES
        XNVMEC_OPT_META_INPUT
        XNVMEC_OPT_META_OUTPUT
        XNVMEC_OPT_LBAF
        XNVMEC_OPT_SLBA
        XNVMEC_OPT_ELBA
        XNVMEC_OPT_LBA
        XNVMEC_OPT_NLB
        XNVMEC_OPT_URI
        XNVMEC_OPT_SYS_URI
        XNVMEC_OPT_UUID
        XNVMEC_OPT_NSID
        XNVMEC_OPT_CNS
        XNVMEC_OPT_CSI
        XNVMEC_OPT_INDEX
        XNVMEC_OPT_SETID
        XNVMEC_OPT_CNTID
        XNVMEC_OPT_LID
        XNVMEC_OPT_LSP
        XNVMEC_OPT_LPO_NBYTES
        XNVMEC_OPT_RAE
        XNVMEC_OPT_CLEAR
        XNVMEC_OPT_ZF
        XNVMEC_OPT_SES
        XNVMEC_OPT_SEL
        XNVMEC_OPT_MSET
        XNVMEC_OPT_AUSE
        XNVMEC_OPT_OVRPAT
        XNVMEC_OPT_OWPASS
        XNVMEC_OPT_OIPBP
        XNVMEC_OPT_NODAS
        XNVMEC_OPT_ACTION
        XNVMEC_OPT_ZRMS
        XNVMEC_OPT_PI
        XNVMEC_OPT_PIL
        XNVMEC_OPT_FID
        XNVMEC_OPT_FEAT
        XNVMEC_OPT_SEED
        XNVMEC_OPT_LIMIT
        XNVMEC_OPT_IOSIZE
        XNVMEC_OPT_QDEPTH
        XNVMEC_OPT_DIRECT
        XNVMEC_OPT_STATUS
        XNVMEC_OPT_SAVE
        XNVMEC_OPT_RESET
        XNVMEC_OPT_VERBOSE
        XNVMEC_OPT_HELP
        XNVMEC_OPT_COUNT
        XNVMEC_OPT_OFFSET
        XNVMEC_OPT_OPCODE
        XNVMEC_OPT_FLAGS
        XNVMEC_OPT_ALL
        XNVMEC_OPT_BE
        XNVMEC_OPT_MEM
        XNVMEC_OPT_SYNC
        XNVMEC_OPT_ASYNC
        XNVMEC_OPT_ADMIN
        XNVMEC_OPT_SHM_ID
        XNVMEC_OPT_MAIN_CORE
        XNVMEC_OPT_CORE_MASK
        XNVMEC_OPT_USE_CMB_SQS
        XNVMEC_OPT_CSS
        XNVMEC_OPT_POLL_IO
        XNVMEC_OPT_POLL_SQ
        XNVMEC_OPT_REGISTER_FILES
        XNVMEC_OPT_REGISTER_BUFFERS
        XNVMEC_OPT_TRUNCATE
        XNVMEC_OPT_RDONLY
        XNVMEC_OPT_WRONLY
        XNVMEC_OPT_RDWR
        XNVMEC_OPT_CREATE
        XNVMEC_OPT_CREATE_MODE
        XNVMEC_OPT_OFLAGS
        XNVMEC_OPT_ADRFAM
        XNVMEC_OPT_DEV_NSID
        XNVMEC_OPT_VEC_CNT
        XNVMEC_OPT_END

    cpdef enum xnvmec_opt_type:
        XNVMEC_POSA
        XNVMEC_LFLG
        XNVMEC_LOPT
        XNVMEC_LREQ

    cpdef enum xnvmec_opt_value_type:
        XNVMEC_OPT_VTYPE_URI
        XNVMEC_OPT_VTYPE_NUM
        XNVMEC_OPT_VTYPE_HEX
        XNVMEC_OPT_VTYPE_FILE
        XNVMEC_OPT_VTYPE_STR

    cdef struct xnvmec_opt_attr:
        xnvmec_opt opt
        xnvmec_opt_value_type vtype
        char* name
        char* descr
        char getoptval

    xnvmec_opt_attr* xnvmec_get_opt_attr(xnvmec_opt opt)

    cdef struct xnvmec_sub_opt:
        xnvmec_opt opt
        xnvmec_opt_type type

    cdef struct xnvmec

    ctypedef int (*xnvmec_subfunc)(xnvmec*)

    cdef struct xnvmec_sub:
        char* name
        char* descr_short
        char* descr_long
        xnvmec_subfunc command
        xnvmec_sub_opt opts[200]

    ctypedef int (*_xnvmec_ver_pr_ft)(int)

    cdef struct xnvmec:
        char* title
        char* descr_short
        char* descr_long
        int nsubs
        xnvmec_sub* subs
        _xnvmec_ver_pr_ft ver_pr
        int argc
        char** argv
        xnvmec_args args
        int given[98]
        xnvmec_sub* sub
        xnvme_timer timer

    cpdef enum xnvmec_opts:
        XNVMEC_INIT_NONE
        XNVMEC_INIT_DEV_OPEN

    cdef struct xnvme_enumeration:
        uint32_t capacity
        uint32_t nentries
        xnvme_ident entries[1]

    int xnvme_enumeration_alloc(xnvme_enumeration** list, uint32_t capacity)

    void xnvme_enumeration_free(xnvme_enumeration* list)

    int xnvme_enumeration_append(xnvme_enumeration* list, xnvme_ident* entry)

    uint64_t xnvmec_timer_start(xnvmec* cli)

    uint64_t xnvmec_timer_stop(xnvmec* cli)

    void xnvmec_timer_bw_pr(xnvmec* cli, char* prefix, size_t nbytes)

    void xnvmec_pinf(char* format)

    void xnvmec_perr(char* msg, int err)

    int xnvmec(xnvmec* cli, int argc, char** argv, int opts)

    int xnvmec_cli_to_opts(xnvmec* cli, xnvme_opts* opts)

    cpdef enum xnvme_pr:
        XNVME_PR_DEF
        XNVME_PR_YAML
        XNVME_PR_TERSE

    int xnvme_be_attr_fpr(void* stream, xnvme_be_attr* attr, int opts)

    int xnvme_be_attr_pr(xnvme_be_attr* attr, int opts)

    int xnvme_be_attr_list_fpr(void* stream, xnvme_be_attr_list* list, int opts)

    int xnvme_be_attr_list_pr(xnvme_be_attr_list* list, int opts)

    int xnvme_lba_fpr(void* stream, uint64_t lba, xnvme_pr opts)

    int xnvme_lba_pr(uint64_t lba, xnvme_pr opts)

    int xnvme_lba_fprn(void* stream, uint64_t* lba, uint16_t nlb, xnvme_pr opts)

    int xnvme_lba_prn(uint64_t* lba, uint16_t nlb, xnvme_pr opts)

    int xnvme_ident_yaml(void* stream, xnvme_ident* ident, int indent, char* sep, int head)

    int xnvme_ident_fpr(void* stream, xnvme_ident* ident, int opts)

    int xnvme_ident_pr(xnvme_ident* ident, int opts)

    cdef struct xnvme_enumeration

    int xnvme_enumeration_fpr(void* stream, xnvme_enumeration* list, int opts)

    int xnvme_enumeration_fpp(void* stream, xnvme_enumeration* list, int opts)

    int xnvme_enumeration_pp(xnvme_enumeration* list, int opts)

    int xnvme_enumeration_pr(xnvme_enumeration* list, int opts)

    int xnvme_dev_fpr(void* stream, xnvme_dev* dev, int opts)

    int xnvme_dev_pr(xnvme_dev* dev, int opts)

    int xnvme_geo_fpr(void* stream, xnvme_geo* geo, int opts)

    int xnvme_geo_pr(xnvme_geo* geo, int opts)

    void xnvme_cmd_ctx_pr(xnvme_cmd_ctx* ctx, int UNUSED_opts)

    int xnvme_opts_pr(xnvme_opts* opts, int pr_opts)
