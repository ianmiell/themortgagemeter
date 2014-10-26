--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	log entry	admin	logentry
9	turl	themortgagemeterapp	turl
10	tmortgage	themortgagemeterapp	tmortgage
11	tinstitution	themortgagemeterapp	tinstitution
15	tmortgagejrnl	themortgagemeterapp	tmortgagejrnl
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add log entry	8	add_logentry
23	Can change log entry	8	change_logentry
24	Can delete log entry	8	delete_logentry
25	Can add turl	9	add_turl
26	Can change turl	9	change_turl
27	Can delete turl	9	delete_turl
28	Can add tmortgage	10	add_tmortgage
29	Can change tmortgage	10	change_tmortgage
30	Can delete tmortgage	10	delete_tmortgage
31	Can add tinstitution	11	add_tinstitution
32	Can change tinstitution	11	change_tinstitution
33	Can delete tinstitution	11	delete_tinstitution
43	Can add tmortgagejrnl	15	add_tmortgagejrnl
44	Can change tmortgagejrnl	15	change_tmortgagejrnl
45	Can delete tmortgagejrnl	15	delete_tmortgagejrnl
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
1	themortgagemeter			MORTGAGECOMPARISON_ADMINEMAIL	sha1$0f1e7$3404dac4ebf4c7faa7ab031716a637bb3b89049a	t	t	t	2012-07-17 08:30:07.758385+00	2012-07-17 08:30:07.758385+00
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('auth_message_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('auth_permission_id_seq', 45, true);


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('django_content_type_id_seq', 15, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Data for Name: matviews; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY matviews (mv_name, v_name, last_refresh) FROM stdin;
replacement_savings_materialized_view	replacement_savings_view	2013-07-17 20:23:57.373464+00
replacement_mortgages_materialized_view	replacement_mortgages_view	2014-10-08 16:00:30.111091+00
\.


--
-- Data for Name: themortgagemeterapp_tmortgage; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY themortgagemeterapp_tmortgage (mortgage_id, institution_code, mortgage_type, rate, apr, ltv, initial_period, booking_fee, term, eligibility) FROM stdin;
\.


--
-- Data for Name: replacement_mortgages_materialized_view; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY replacement_mortgages_materialized_view (change_date, institution_code, mortgage_type, eligibility, ltv, initial_period, booking_fee, cr_date, delete_date, rate, svr, apr, last_retrieved, mortgage_id, institution_name, url, action_type) FROM stdin;
\.


--
-- Data for Name: replacement_savings_materialized_view; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY replacement_savings_materialized_view (change_date, institution_code, variability, isa, child, online, branch, interest_paid, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, savings_period, min_amt, max_amt, gross_percent, aer_percent, last_retrieved, institution_name, url, action_type) FROM stdin;
\.


--
-- Data for Name: talert; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY talert (alert_id, cr_date, alert, status) FROM stdin;
\.


--
-- Name: talert_alert_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('talert_alert_id_seq', 1854, true);


--
-- Name: tinsertcurrentmortgage_insert_current_mortgage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('tinsertcurrentmortgage_insert_current_mortgage_id_seq', 21673, true);


--
-- Data for Name: tinstitution; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY tinstitution (institution_code, institution_type, institution_name, mortgage_status) FROM stdin;
HSBC	BANK	HSBC	A
NTNWD	BANK	Nationwide	A
LLOYDS	BANK	Lloyds Bank	A
HLFX	BANK	Halifax	A
NRTHNR	BANK	Northern Rock	S
SNTNDR	BANK	Santander	A
CHLS	BANK	Chelsea Building Society	A
TSC	BANK	Tesco Bank	A
SKPTN	BANK	Skipton Building Society	A
NTWST	BANK	NatWest	A
PSTFFC	BANK	The Post Office	S
YRKSHR	BANK	Yorkshire Building Society	A
\.


--
-- Data for Name: tmailsubscriber; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY tmailsubscriber (email_address, cr_date) FROM stdin;
\.


--
-- Data for Name: tmortgage; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY tmortgage (mortgage_id, institution_code, mortgage_type, rate, apr, ltv, initial_period, booking_fee, term, eligibility, svr) FROM stdin;
\.


--
-- Name: tmortgage_mortgage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('tmortgage_mortgage_id_seq', 20443, true);


--
-- Data for Name: tmortgagejrnl; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY tmortgagejrnl (mortgage_jrnl_id, cr_date, mortgage_id, last_retrieved, delete_date, url_id) FROM stdin;
\.


--
-- Data for Name: tretrievaldates; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY tretrievaldates (day) FROM stdin;
\.


--
-- Data for Name: tsavings; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY tsavings (savings_id, institution_code, variability, isa, child, online, branch, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, savings_period, min_amt, max_amt, gross_percent, aer_percent, interest_paid) FROM stdin;
\.


--
-- Name: tsavings_savings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('tsavings_savings_id_seq', 258, true);


--
-- Data for Name: tsavingsjrnl; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY tsavingsjrnl (savings_jrnl_id, cr_date, savings_id, last_retrieved, delete_date, url_id) FROM stdin;
\.


--
-- Name: tsavingsjrnl_savings_jrnl_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('tsavingsjrnl_savings_jrnl_id_seq', 280, true);


--
-- Data for Name: turl; Type: TABLE DATA; Schema: public; Owner: themortgagemeter
--

COPY turl (url_id, url) FROM stdin;
\.


--
-- Name: turl_url_id_seq; Type: SEQUENCE SET; Schema: public; Owner: themortgagemeter
--

SELECT pg_catalog.setval('turl_url_id_seq', 1392, true);


--
-- PostgreSQL database dump complete
--

