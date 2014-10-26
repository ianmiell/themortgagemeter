--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: mortgage_info; Type: SCHEMA; Schema: -; Owner: themortgagemeter
--

CREATE SCHEMA mortgage_info;


ALTER SCHEMA mortgage_info OWNER TO themortgagemeter;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: create_matview(name, name); Type: FUNCTION; Schema: public; Owner: themortgagemeter
--

CREATE FUNCTION create_matview(name, name) RETURNS void
    LANGUAGE plpgsql SECURITY DEFINER
    AS $_$
 DECLARE
     matview ALIAS FOR $1;
     view_name ALIAS FOR $2;
     entry matviews%ROWTYPE;
 BEGIN
     SELECT * INTO entry FROM matviews WHERE mv_name = matview;
 
     IF FOUND THEN
         RAISE EXCEPTION 'Materialized view ''%'' already exists.',
           matview;
     END IF;
 
     EXECUTE 'REVOKE ALL ON ' || view_name || ' FROM PUBLIC'; 
 
     EXECUTE 'GRANT SELECT ON ' || view_name || ' TO PUBLIC';
 
     EXECUTE 'CREATE TABLE ' || matview || ' AS SELECT * FROM ' || view_name;
 
     EXECUTE 'REVOKE ALL ON ' || matview || ' FROM PUBLIC';
 
     EXECUTE 'GRANT SELECT ON ' || matview || ' TO PUBLIC';
 
     INSERT INTO matviews (mv_name, v_name, last_refresh)
       VALUES (matview, view_name, CURRENT_TIMESTAMP); 
     
     RETURN;
 END
 $_$;


ALTER FUNCTION public.create_matview(name, name) OWNER TO themortgagemeter;

--
-- Name: drop_matview(name); Type: FUNCTION; Schema: public; Owner: themortgagemeter
--

CREATE FUNCTION drop_matview(name) RETURNS void
    LANGUAGE plpgsql SECURITY DEFINER
    AS $_$
 DECLARE
     matview ALIAS FOR $1;
     entry matviews%ROWTYPE;
 BEGIN
 
     SELECT * INTO entry FROM matviews WHERE mv_name = matview;
 
     IF NOT FOUND THEN
         RAISE EXCEPTION 'Materialized view % does not exist.', matview;
     END IF;
 
     EXECUTE 'DROP TABLE ' || matview;
     DELETE FROM matviews WHERE mv_name=matview;
 
     RETURN;
 END
 $_$;


ALTER FUNCTION public.drop_matview(name) OWNER TO themortgagemeter;

--
-- Name: refresh_matview(name); Type: FUNCTION; Schema: public; Owner: themortgagemeter
--

CREATE FUNCTION refresh_matview(name) RETURNS void
    LANGUAGE plpgsql SECURITY DEFINER
    AS $_$
 DECLARE 
     matview ALIAS FOR $1;
     entry matviews%ROWTYPE;
 BEGIN
 
     SELECT * INTO entry FROM matviews WHERE mv_name = matview;
 
     IF NOT FOUND THEN
         RAISE EXCEPTION
'Materialized view % does not exist.', matview;
    END IF;

    EXECUTE 'DELETE FROM ' || matview;
    EXECUTE 'INSERT INTO ' || matview
        || ' SELECT * FROM ' || entry.v_name;

    UPDATE matviews
        SET last_refresh=CURRENT_TIMESTAMP
        WHERE mv_name=matview;

    RETURN;
END
$_$;


ALTER FUNCTION public.refresh_matview(name) OWNER TO themortgagemeter;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO themortgagemeter;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO themortgagemeter;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO themortgagemeter;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO themortgagemeter;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.auth_message OWNER TO themortgagemeter;

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_message_id_seq OWNER TO themortgagemeter;

--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO themortgagemeter;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO themortgagemeter;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO themortgagemeter;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO themortgagemeter;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO themortgagemeter;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO themortgagemeter;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO themortgagemeter;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO themortgagemeter;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO themortgagemeter;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO themortgagemeter;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO themortgagemeter;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO themortgagemeter;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO themortgagemeter;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO themortgagemeter;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO themortgagemeter;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: matviews; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE matviews (
    mv_name name NOT NULL,
    v_name name NOT NULL,
    last_refresh timestamp with time zone
);


ALTER TABLE public.matviews OWNER TO themortgagemeter;

--
-- Name: mortgagecomparisonapp_tmortgage; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE mortgagecomparisonapp_tmortgage (
    mortgage_id integer NOT NULL,
    institution_code character varying(6) NOT NULL,
    mortgage_type text NOT NULL,
    rate integer NOT NULL,
    apr integer NOT NULL,
    ltv integer NOT NULL,
    initial_period integer NOT NULL,
    booking_fee integer NOT NULL,
    term integer NOT NULL,
    eligibility character varying(16) NOT NULL
);


ALTER TABLE public.mortgagecomparisonapp_tmortgage OWNER TO themortgagemeter;

--
-- Name: replacement_mortgages_materialized_view; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE replacement_mortgages_materialized_view (
    change_date date,
    institution_code character varying(6),
    mortgage_type character(1),
    eligibility character varying(16),
    ltv integer,
    initial_period integer,
    booking_fee integer,
    cr_date date,
    delete_date date,
    rate integer,
    svr integer,
    apr integer,
    last_retrieved date,
    mortgage_id integer,
    institution_name character varying(100),
    url character varying(200),
    action_type text
);


ALTER TABLE public.replacement_mortgages_materialized_view OWNER TO themortgagemeter;

--
-- Name: tinstitution; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE tinstitution (
    institution_code character varying(6) NOT NULL,
    institution_type character varying(4),
    institution_name character varying(100),
    mortgage_status character(1) DEFAULT 'A'::bpchar
);


ALTER TABLE public.tinstitution OWNER TO themortgagemeter;

--
-- Name: tmortgage; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE tmortgage (
    mortgage_id integer NOT NULL,
    institution_code character varying(6),
    mortgage_type character(1),
    rate integer,
    apr integer,
    ltv integer,
    initial_period integer,
    booking_fee integer,
    term integer,
    eligibility character varying(16),
    svr integer NOT NULL
);


ALTER TABLE public.tmortgage OWNER TO themortgagemeter;

--
-- Name: tmortgagejrnl; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE tmortgagejrnl (
    mortgage_jrnl_id integer NOT NULL,
    cr_date date,
    mortgage_id integer NOT NULL,
    last_retrieved date,
    delete_date date,
    url_id integer
);


ALTER TABLE public.tmortgagejrnl OWNER TO themortgagemeter;

--
-- Name: turl; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE turl (
    url_id integer NOT NULL,
    url character varying(200)
);


ALTER TABLE public.turl OWNER TO themortgagemeter;

--
-- Name: replacement_mortgages_view; Type: VIEW; Schema: public; Owner: themortgagemeter
--

CREATE VIEW replacement_mortgages_view AS
    (SELECT j1.delete_date AS change_date, m1.institution_code, m1.mortgage_type, m1.eligibility, m1.ltv, m1.initial_period, m1.booking_fee, j1.cr_date, j1.delete_date, m1.rate, m1.svr, m1.apr, j1.last_retrieved, m1.mortgage_id, t1.institution_name, u1.url, 'REPLACED'::text AS action_type FROM tmortgage m1, tmortgagejrnl j1, tinstitution t1, turl u1 WHERE (((((m1.mortgage_id = j1.mortgage_id) AND (j1.url_id = u1.url_id)) AND ((t1.institution_code)::text = (m1.institution_code)::text)) AND (j1.delete_date IS NOT NULL)) AND (EXISTS (SELECT 1 FROM tmortgage m2, tmortgagejrnl j2 WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j1.delete_date = j2.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) AND (j2.delete_date IS NULL))))) UNION SELECT j1.cr_date AS change_date, m1.institution_code, m1.mortgage_type, m1.eligibility, m1.ltv, m1.initial_period, m1.booking_fee, j1.cr_date, j1.delete_date, m1.rate, m1.svr, m1.apr, j1.last_retrieved, m1.mortgage_id, t1.institution_name, u1.url, 'REPLACING'::text AS action_type FROM tmortgage m1, tmortgagejrnl j1, tinstitution t1, turl u1 WHERE (((((m1.mortgage_id = j1.mortgage_id) AND (j1.url_id = u1.url_id)) AND (j1.delete_date IS NULL)) AND ((t1.institution_code)::text = (m1.institution_code)::text)) AND (EXISTS (SELECT 1 FROM tmortgagejrnl j2, tmortgage m2 WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j2.delete_date = j1.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) AND (j2.delete_date IS NOT NULL)))))) UNION SELECT CASE WHEN (j1.delete_date IS NULL) THEN j1.cr_date WHEN (j1.delete_date IS NOT NULL) THEN j1.delete_date ELSE NULL::date END AS change_date, m1.institution_code, m1.mortgage_type, m1.eligibility, m1.ltv, m1.initial_period, m1.booking_fee, j1.cr_date, j1.delete_date, m1.rate, m1.svr, m1.apr, j1.last_retrieved, m1.mortgage_id, t1.institution_name, u1.url, CASE WHEN (j1.delete_date IS NULL) THEN 'ADDED'::text WHEN (j1.delete_date IS NOT NULL) THEN 'DELETED'::text ELSE NULL::text END AS action_type FROM tmortgage m1, tmortgagejrnl j1, tinstitution t1, turl u1 WHERE ((((m1.mortgage_id = j1.mortgage_id) AND (u1.url_id = j1.url_id)) AND ((t1.institution_code)::text = (m1.institution_code)::text)) AND (NOT (m1.mortgage_id IN (SELECT m1.mortgage_id FROM tmortgage m1, tmortgagejrnl j1 WHERE (((m1.mortgage_id = j1.mortgage_id) AND (j1.delete_date IS NOT NULL)) AND (EXISTS (SELECT 1 FROM tmortgage m2, tmortgagejrnl j2 WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j1.delete_date = j2.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) AND (j2.delete_date IS NULL))))) UNION SELECT m1.mortgage_id FROM tmortgage m1, tmortgagejrnl j1 WHERE (((m1.mortgage_id = j1.mortgage_id) AND (j1.delete_date IS NULL)) AND (EXISTS (SELECT 1 FROM tmortgagejrnl j2, tmortgage m2 WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j2.delete_date = j1.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) AND (j2.delete_date IS NOT NULL))))))))) ORDER BY 1 DESC, 2, 3, 4, 5, 6, 13, 10, 7;


ALTER TABLE public.replacement_mortgages_view OWNER TO themortgagemeter;

--
-- Name: replacement_savings_materialized_view; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE replacement_savings_materialized_view (
    change_date date,
    institution_code character varying(6),
    variability character(1),
    isa character(1),
    child character(1),
    online character(1),
    branch character(1),
    interest_paid character(1),
    regular_saver character(1),
    regular_saver_frequency_period integer,
    regular_saver_frequency_type character(1),
    regular_saver_min_amt integer,
    regular_saver_max_amt integer,
    bonus character(1),
    bonus_frequency_period integer,
    bonus_frequency_type character(1),
    savings_period integer,
    min_amt integer,
    max_amt integer,
    gross_percent integer,
    aer_percent integer,
    last_retrieved date,
    institution_name character varying(100),
    url character varying(200),
    action_type text
);


ALTER TABLE public.replacement_savings_materialized_view OWNER TO themortgagemeter;

--
-- Name: tsavings; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE tsavings (
    savings_id integer NOT NULL,
    institution_code character varying(6),
    variability character(1) DEFAULT 'V'::bpchar,
    isa character(1) DEFAULT 'N'::bpchar NOT NULL,
    child character(1) DEFAULT 'N'::bpchar NOT NULL,
    online character(1) DEFAULT 'N'::bpchar NOT NULL,
    branch character(1) DEFAULT 'N'::bpchar NOT NULL,
    regular_saver character(1) DEFAULT 'N'::bpchar NOT NULL,
    regular_saver_frequency_period integer DEFAULT (-1),
    regular_saver_frequency_type character(1) DEFAULT 'M'::bpchar,
    regular_saver_min_amt integer DEFAULT (-1),
    regular_saver_max_amt integer DEFAULT (-1),
    bonus character(1) DEFAULT 'N'::bpchar NOT NULL,
    bonus_frequency_period integer DEFAULT (-1),
    bonus_frequency_type character(1) DEFAULT 'M'::bpchar,
    savings_period integer DEFAULT (-1),
    min_amt integer DEFAULT (-1),
    max_amt integer DEFAULT (-1),
    gross_percent integer NOT NULL,
    aer_percent integer NOT NULL,
    interest_paid character(1) DEFAULT 'U'::bpchar,
    CONSTRAINT tsavings_c1 CHECK ((((((regular_saver = 'N'::bpchar) AND (regular_saver_min_amt < 0)) AND (regular_saver_max_amt < 0)) AND (regular_saver_frequency_period < 0)) OR ((((regular_saver = 'Y'::bpchar) AND (regular_saver_min_amt >= 0)) AND (regular_saver_max_amt > regular_saver_min_amt)) AND (regular_saver_frequency_period > 0)))),
    CONSTRAINT tsavings_c2 CHECK ((((bonus = 'N'::bpchar) AND (bonus_frequency_period < 0)) OR ((bonus = 'Y'::bpchar) AND (bonus_frequency_period > 0)))),
    CONSTRAINT tsavings_c3 CHECK ((((((((((min_amt >= 0) AND (variability = ANY (ARRAY['V'::bpchar, 'F'::bpchar]))) AND (interest_paid = ANY (ARRAY['Y'::bpchar, 'M'::bpchar, 'U'::bpchar]))) AND (branch = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))) AND (online = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))) AND (bonus = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))) AND (isa = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))) AND (regular_saver = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))) AND (child = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))))
);


ALTER TABLE public.tsavings OWNER TO themortgagemeter;

--
-- Name: tsavingsjrnl; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE tsavingsjrnl (
    savings_jrnl_id integer NOT NULL,
    cr_date date,
    savings_id integer NOT NULL,
    last_retrieved date,
    delete_date date,
    url_id integer
);


ALTER TABLE public.tsavingsjrnl OWNER TO themortgagemeter;

--
-- Name: replacement_savings_view; Type: VIEW; Schema: public; Owner: themortgagemeter
--

CREATE VIEW replacement_savings_view AS
    (SELECT j1.delete_date AS change_date, s1.institution_code, s1.variability, s1.isa, s1.child, s1.online, s1.branch, s1.interest_paid, s1.regular_saver, s1.regular_saver_frequency_period, s1.regular_saver_frequency_type, s1.regular_saver_min_amt, s1.regular_saver_max_amt, s1.bonus, s1.bonus_frequency_period, s1.bonus_frequency_type, s1.savings_period, s1.min_amt, s1.max_amt, s1.gross_percent, s1.aer_percent, j1.last_retrieved, t1.institution_name, u1.url, 'REPLACED'::text AS action_type FROM tsavings s1, tsavingsjrnl j1, tinstitution t1, turl u1 WHERE (((((s1.savings_id = j1.savings_id) AND ((s1.institution_code)::text = (t1.institution_code)::text)) AND (j1.delete_date IS NOT NULL)) AND (u1.url_id = j1.url_id)) AND (EXISTS (SELECT 1 FROM tsavings s2, tsavingsjrnl j2 WHERE (((((((((((((((((((s2.savings_id = j2.savings_id) AND (j1.delete_date = j2.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) AND (s2.variability = s1.variability)) AND (s1.isa = s2.isa)) AND (s1.child = s2.child)) AND (s1.regular_saver = s2.regular_saver)) AND (s1.regular_saver_frequency_period = s2.regular_saver_frequency_period)) AND (s1.regular_saver_frequency_type = s2.regular_saver_frequency_type)) AND (s1.regular_saver_min_amt = s2.regular_saver_min_amt)) AND (s1.regular_saver_max_amt = s2.regular_saver_max_amt)) AND (s1.bonus = s2.bonus)) AND (s1.bonus_frequency_period = s2.bonus_frequency_period)) AND (s1.bonus_frequency_type = s2.bonus_frequency_type)) AND (s1.savings_period = s2.savings_period)) AND (s1.min_amt = s2.min_amt)) AND (s1.max_amt = s2.max_amt)) AND (s1.interest_paid = s2.interest_paid)) AND (j2.delete_date IS NULL))))) UNION SELECT j1.cr_date AS change_date, s1.institution_code, s1.variability, s1.isa, s1.child, s1.online, s1.branch, s1.interest_paid, s1.regular_saver, s1.regular_saver_frequency_period, s1.regular_saver_frequency_type, s1.regular_saver_min_amt, s1.regular_saver_max_amt, s1.bonus, s1.bonus_frequency_period, s1.bonus_frequency_type, s1.savings_period, s1.min_amt, s1.max_amt, s1.gross_percent, s1.aer_percent, j1.last_retrieved, t1.institution_name, u1.url, 'REPLACING'::text AS action_type FROM tsavings s1, tsavingsjrnl j1, tinstitution t1, turl u1 WHERE (((((s1.savings_id = j1.savings_id) AND ((s1.institution_code)::text = (t1.institution_code)::text)) AND (j1.delete_date IS NULL)) AND (u1.url_id = j1.url_id)) AND (EXISTS (SELECT 1 FROM tsavings s2, tsavingsjrnl j2 WHERE (((((((((((((((((((s2.savings_id = j2.savings_id) AND (j2.delete_date = j1.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) AND (s2.variability = s1.variability)) AND (s1.isa = s2.isa)) AND (s1.child = s2.child)) AND (s1.regular_saver = s2.regular_saver)) AND (s1.regular_saver_frequency_period = s2.regular_saver_frequency_period)) AND (s1.regular_saver_frequency_type = s2.regular_saver_frequency_type)) AND (s1.regular_saver_min_amt = s2.regular_saver_min_amt)) AND (s1.regular_saver_max_amt = s2.regular_saver_max_amt)) AND (s1.bonus = s2.bonus)) AND (s1.bonus_frequency_period = s2.bonus_frequency_period)) AND (s1.bonus_frequency_type = s2.bonus_frequency_type)) AND (s1.savings_period = s2.savings_period)) AND (s1.min_amt = s2.min_amt)) AND (s1.max_amt = s2.max_amt)) AND (s1.interest_paid = s2.interest_paid)) AND (j2.delete_date IS NOT NULL)))))) UNION SELECT CASE WHEN (j1.delete_date IS NULL) THEN j1.cr_date WHEN (j1.delete_date IS NOT NULL) THEN j1.delete_date ELSE NULL::date END AS change_date, s1.institution_code, s1.variability, s1.isa, s1.child, s1.online, s1.branch, s1.interest_paid, s1.regular_saver, s1.regular_saver_frequency_period, s1.regular_saver_frequency_type, s1.regular_saver_min_amt, s1.regular_saver_max_amt, s1.bonus, s1.bonus_frequency_period, s1.bonus_frequency_type, s1.savings_period, s1.min_amt, s1.max_amt, s1.gross_percent, s1.aer_percent, j1.last_retrieved, t1.institution_name, u1.url, CASE WHEN (j1.delete_date IS NULL) THEN 'ADDED'::text WHEN (j1.delete_date IS NOT NULL) THEN 'DELETED'::text ELSE NULL::text END AS action_type FROM tsavings s1, tsavingsjrnl j1, tinstitution t1, turl u1 WHERE ((((s1.savings_id = j1.savings_id) AND (u1.url_id = j1.url_id)) AND ((t1.institution_code)::text = (s1.institution_code)::text)) AND (NOT (s1.savings_id IN (SELECT s1.savings_id FROM tsavings s1, tsavingsjrnl j1 WHERE (((s1.savings_id = j1.savings_id) AND (j1.delete_date IS NOT NULL)) AND (EXISTS (SELECT 1 FROM tsavings s2, tsavingsjrnl j2 WHERE (((((((((((((((((((s2.savings_id = j2.savings_id) AND (j1.delete_date = j2.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) AND (s2.variability = s1.variability)) AND (s1.isa = s2.isa)) AND (s1.child = s2.child)) AND (s1.regular_saver = s2.regular_saver)) AND (s1.regular_saver_frequency_period = s2.regular_saver_frequency_period)) AND (s1.regular_saver_frequency_type = s2.regular_saver_frequency_type)) AND (s1.regular_saver_min_amt = s2.regular_saver_min_amt)) AND (s1.regular_saver_max_amt = s2.regular_saver_max_amt)) AND (s1.bonus = s2.bonus)) AND (s1.bonus_frequency_period = s2.bonus_frequency_period)) AND (s1.bonus_frequency_type = s2.bonus_frequency_type)) AND (s1.savings_period = s2.savings_period)) AND (s1.min_amt = s2.min_amt)) AND (s1.max_amt = s2.max_amt)) AND (s1.interest_paid = s2.interest_paid)) AND (j2.delete_date IS NULL))))) UNION SELECT s1.savings_id FROM tsavings s1, tsavingsjrnl j1 WHERE (((s1.savings_id = j1.savings_id) AND (j1.delete_date IS NULL)) AND (EXISTS (SELECT 1 FROM tsavingsjrnl j2, tsavings s2 WHERE ((((((((((((((((((((s2.savings_id = j2.savings_id) AND (j2.delete_date = j1.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) AND (s2.variability = s1.variability)) AND (s1.isa = s2.isa)) AND (s1.child = s2.child)) AND (s1.regular_saver = s2.regular_saver)) AND (s1.regular_saver_frequency_period = s2.regular_saver_frequency_period)) AND (s1.regular_saver_frequency_type = s2.regular_saver_frequency_type)) AND (s1.regular_saver_min_amt = s2.regular_saver_min_amt)) AND (s1.regular_saver_max_amt = s2.regular_saver_max_amt)) AND (s1.bonus = s2.bonus)) AND (s1.bonus_frequency_period = s2.bonus_frequency_period)) AND (s1.bonus_frequency_type = s2.bonus_frequency_type)) AND (s1.savings_period = s2.savings_period)) AND (s1.min_amt = s2.min_amt)) AND (s1.max_amt = s2.max_amt)) AND (s1.interest_paid = s2.interest_paid)) AND (j2.delete_date IS NOT NULL)) AND (j2.delete_date IS NOT NULL))))))))) ORDER BY 1 DESC, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 22, 20;


ALTER TABLE public.replacement_savings_view OWNER TO themortgagemeter;

--
-- Name: talert; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE talert (
    alert_id integer NOT NULL,
    cr_date timestamp without time zone DEFAULT now(),
    alert text,
    status character(1) DEFAULT 'A'::bpchar NOT NULL
);


ALTER TABLE public.talert OWNER TO themortgagemeter;

--
-- Name: talert_alert_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE talert_alert_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.talert_alert_id_seq OWNER TO themortgagemeter;

--
-- Name: talert_alert_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE talert_alert_id_seq OWNED BY talert.alert_id;


--
-- Name: tinsertcurrentmortgage_insert_current_mortgage_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE tinsertcurrentmortgage_insert_current_mortgage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tinsertcurrentmortgage_insert_current_mortgage_id_seq OWNER TO themortgagemeter;

--
-- Name: tinsertcurrentmortgage_insert_current_mortgage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE tinsertcurrentmortgage_insert_current_mortgage_id_seq OWNED BY tmortgagejrnl.mortgage_jrnl_id;


--
-- Name: tmailsubscriber; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE tmailsubscriber (
    email_address text NOT NULL,
    cr_date timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tmailsubscriber OWNER TO themortgagemeter;

--
-- Name: tmortgage_mortgage_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE tmortgage_mortgage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tmortgage_mortgage_id_seq OWNER TO themortgagemeter;

--
-- Name: tmortgage_mortgage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE tmortgage_mortgage_id_seq OWNED BY tmortgage.mortgage_id;


--
-- Name: tretrievaldates; Type: TABLE; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE TABLE tretrievaldates (
    day date NOT NULL
);


ALTER TABLE public.tretrievaldates OWNER TO themortgagemeter;

--
-- Name: tsavings_savings_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE tsavings_savings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tsavings_savings_id_seq OWNER TO themortgagemeter;

--
-- Name: tsavings_savings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE tsavings_savings_id_seq OWNED BY tsavings.savings_id;


--
-- Name: tsavingsjrnl_savings_jrnl_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE tsavingsjrnl_savings_jrnl_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tsavingsjrnl_savings_jrnl_id_seq OWNER TO themortgagemeter;

--
-- Name: tsavingsjrnl_savings_jrnl_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE tsavingsjrnl_savings_jrnl_id_seq OWNED BY tsavingsjrnl.savings_jrnl_id;


--
-- Name: turl_url_id_seq; Type: SEQUENCE; Schema: public; Owner: themortgagemeter
--

CREATE SEQUENCE turl_url_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.turl_url_id_seq OWNER TO themortgagemeter;

--
-- Name: turl_url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: themortgagemeter
--

ALTER SEQUENCE turl_url_id_seq OWNED BY turl.url_id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: alert_id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY talert ALTER COLUMN alert_id SET DEFAULT nextval('talert_alert_id_seq'::regclass);


--
-- Name: mortgage_id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY tmortgage ALTER COLUMN mortgage_id SET DEFAULT nextval('tmortgage_mortgage_id_seq'::regclass);


--
-- Name: mortgage_jrnl_id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY tmortgagejrnl ALTER COLUMN mortgage_jrnl_id SET DEFAULT nextval('tinsertcurrentmortgage_insert_current_mortgage_id_seq'::regclass);


--
-- Name: savings_id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY tsavings ALTER COLUMN savings_id SET DEFAULT nextval('tsavings_savings_id_seq'::regclass);


--
-- Name: savings_jrnl_id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY tsavingsjrnl ALTER COLUMN savings_jrnl_id SET DEFAULT nextval('tsavingsjrnl_savings_jrnl_id_seq'::regclass);


--
-- Name: url_id; Type: DEFAULT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY turl ALTER COLUMN url_id SET DEFAULT nextval('turl_url_id_seq'::regclass);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: matviews_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY matviews
    ADD CONSTRAINT matviews_pkey PRIMARY KEY (mv_name);


--
-- Name: mortgagecomparisonapp_tmortgage_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY mortgagecomparisonapp_tmortgage
    ADD CONSTRAINT mortgagecomparisonapp_tmortgage_pkey PRIMARY KEY (mortgage_id);


--
-- Name: retrieval_dates_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY tretrievaldates
    ADD CONSTRAINT retrieval_dates_pkey PRIMARY KEY (day);


--
-- Name: tinsertcurrentmortgage_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY tmortgagejrnl
    ADD CONSTRAINT tinsertcurrentmortgage_pkey PRIMARY KEY (mortgage_jrnl_id);


--
-- Name: tinstitution_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY tinstitution
    ADD CONSTRAINT tinstitution_pkey PRIMARY KEY (institution_code);


--
-- Name: tmailsubscriber_email_address_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY tmailsubscriber
    ADD CONSTRAINT tmailsubscriber_email_address_key UNIQUE (email_address);


--
-- Name: tmortgage_institution_code_mortgage_type_rate_apr_ltv_initial_p; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY tmortgage
    ADD CONSTRAINT tmortgage_institution_code_mortgage_type_rate_apr_ltv_initial_p UNIQUE (institution_code, mortgage_type, rate, apr, ltv, initial_period, booking_fee, term, eligibility, svr);


--
-- Name: tmortgage_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY tmortgage
    ADD CONSTRAINT tmortgage_pkey PRIMARY KEY (mortgage_id);


--
-- Name: tsavings_institution_code_mortgage_type_rate_apr_ltv_initial_p; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY tsavings
    ADD CONSTRAINT tsavings_institution_code_mortgage_type_rate_apr_ltv_initial_p UNIQUE (institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, interest_paid, child);


--
-- Name: turl_pkey; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY turl
    ADD CONSTRAINT turl_pkey PRIMARY KEY (url_id);


--
-- Name: turl_url_key; Type: CONSTRAINT; Schema: public; Owner: themortgagemeter; Tablespace: 
--

ALTER TABLE ONLY turl
    ADD CONSTRAINT turl_url_key UNIQUE (url);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: tmortgage_mortgage_id_idx; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE UNIQUE INDEX tmortgage_mortgage_id_idx ON tmortgage USING btree (mortgage_id);


--
-- Name: tmortgagejrnl_mortgage_id_idx; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE INDEX tmortgagejrnl_mortgage_id_idx ON tmortgagejrnl USING btree (mortgage_id);


--
-- Name: tsavings_savings_id_idx; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE UNIQUE INDEX tsavings_savings_id_idx ON tsavings USING btree (savings_id);


--
-- Name: tsavingsjrnl_savings_jrnl_id_idx; Type: INDEX; Schema: public; Owner: themortgagemeter; Tablespace: 
--

CREATE UNIQUE INDEX tsavingsjrnl_savings_jrnl_id_idx ON tsavingsjrnl USING btree (savings_jrnl_id);


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tinsertcurrentmortgage_mortgage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY tmortgagejrnl
    ADD CONSTRAINT tinsertcurrentmortgage_mortgage_id_fkey FOREIGN KEY (mortgage_id) REFERENCES tmortgage(mortgage_id);


--
-- Name: tsavingsjrnl_savings_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY tsavingsjrnl
    ADD CONSTRAINT tsavingsjrnl_savings_id_fkey FOREIGN KEY (savings_id) REFERENCES tsavings(savings_id);


--
-- Name: user_id_refs_id_7ceef80f; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_7ceef80f FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_dfbab7d; Type: FK CONSTRAINT; Schema: public; Owner: themortgagemeter
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_dfbab7d FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: replacement_mortgages_materialized_view; Type: ACL; Schema: public; Owner: themortgagemeter
--

REVOKE ALL ON TABLE replacement_mortgages_materialized_view FROM PUBLIC;
REVOKE ALL ON TABLE replacement_mortgages_materialized_view FROM themortgagemeter;
GRANT ALL ON TABLE replacement_mortgages_materialized_view TO themortgagemeter;
GRANT SELECT ON TABLE replacement_mortgages_materialized_view TO PUBLIC;


--
-- Name: replacement_mortgages_view; Type: ACL; Schema: public; Owner: themortgagemeter
--

REVOKE ALL ON TABLE replacement_mortgages_view FROM PUBLIC;
REVOKE ALL ON TABLE replacement_mortgages_view FROM themortgagemeter;
GRANT ALL ON TABLE replacement_mortgages_view TO themortgagemeter;
GRANT SELECT ON TABLE replacement_mortgages_view TO PUBLIC;


--
-- Name: replacement_savings_materialized_view; Type: ACL; Schema: public; Owner: themortgagemeter
--

REVOKE ALL ON TABLE replacement_savings_materialized_view FROM PUBLIC;
REVOKE ALL ON TABLE replacement_savings_materialized_view FROM themortgagemeter;
GRANT ALL ON TABLE replacement_savings_materialized_view TO themortgagemeter;
GRANT SELECT ON TABLE replacement_savings_materialized_view TO PUBLIC;


--
-- Name: replacement_savings_view; Type: ACL; Schema: public; Owner: themortgagemeter
--

REVOKE ALL ON TABLE replacement_savings_view FROM PUBLIC;
REVOKE ALL ON TABLE replacement_savings_view FROM themortgagemeter;
GRANT ALL ON TABLE replacement_savings_view TO themortgagemeter;
GRANT SELECT ON TABLE replacement_savings_view TO PUBLIC;


--
-- PostgreSQL database dump complete
--

