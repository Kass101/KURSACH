PGDMP  1    #                }            BD_CPK    17.4    17.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16484    BD_CPK    DATABASE     n   CREATE DATABASE "BD_CPK" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ru-RU';
    DROP DATABASE "BD_CPK";
                     postgres    false            �            1259    16485    Class    TABLE     (  CREATE TABLE public."Class" (
    id_class integer NOT NULL,
    date_time timestamp without time zone NOT NULL,
    type character varying(25) NOT NULL,
    shifr character varying(10) NOT NULL,
    id_professor character varying(10) NOT NULL,
    class_number character varying(10) NOT NULL
);
    DROP TABLE public."Class";
       public         heap r       postgres    false            �            1259    16588    Class_id_class_seq    SEQUENCE     �   ALTER TABLE public."Class" ALTER COLUMN id_class ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Class_id_class_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    217            �            1259    16503    Course    TABLE     �   CREATE TABLE public."Course" (
    id_course character varying(12) NOT NULL,
    name character varying(50) NOT NULL,
    hours integer NOT NULL
);
    DROP TABLE public."Course";
       public         heap r       postgres    false            �            1259    16491    Group    TABLE     �   CREATE TABLE public."Group" (
    shifr character varying(10) NOT NULL,
    id_course character varying(12) NOT NULL,
    begin_date date NOT NULL,
    end_date date NOT NULL
);
    DROP TABLE public."Group";
       public         heap r       postgres    false            �            1259    16494 	   Professor    TABLE     �   CREATE TABLE public."Professor" (
    id_professor character varying(10) NOT NULL,
    fio character varying(100) NOT NULL,
    phone_number character varying(11) NOT NULL,
    email character varying(50) NOT NULL
);
    DROP TABLE public."Professor";
       public         heap r       postgres    false            �            1259    16497    Student    TABLE     �  CREATE TABLE public."Student" (
    id_student character varying(10) NOT NULL,
    date date NOT NULL,
    fio character varying(100) NOT NULL,
    series character varying(4) NOT NULL,
    number character varying(6) NOT NULL,
    issued_by character varying(50) NOT NULL,
    phone_number character varying(11) NOT NULL,
    email character varying(50) NOT NULL,
    organisation character varying(100) NOT NULL,
    "position" character varying(50) NOT NULL,
    date_of_issue date NOT NULL
);
    DROP TABLE public."Student";
       public         heap r       postgres    false            �            1259    16500    Student_Group    TABLE     �   CREATE TABLE public."Student_Group" (
    id_student character varying(10) NOT NULL,
    shifr character varying(10) NOT NULL
);
 #   DROP TABLE public."Student_Group";
       public         heap r       postgres    false            �          0    16485    Class 
   TABLE DATA           _   COPY public."Class" (id_class, date_time, type, shifr, id_professor, class_number) FROM stdin;
    public               postgres    false    217   %       �          0    16503    Course 
   TABLE DATA           :   COPY public."Course" (id_course, name, hours) FROM stdin;
    public               postgres    false    222   �%       �          0    16491    Group 
   TABLE DATA           I   COPY public."Group" (shifr, id_course, begin_date, end_date) FROM stdin;
    public               postgres    false    218   j&       �          0    16494 	   Professor 
   TABLE DATA           M   COPY public."Professor" (id_professor, fio, phone_number, email) FROM stdin;
    public               postgres    false    219   �&       �          0    16497    Student 
   TABLE DATA           �   COPY public."Student" (id_student, date, fio, series, number, issued_by, phone_number, email, organisation, "position", date_of_issue) FROM stdin;
    public               postgres    false    220   s'       �          0    16500    Student_Group 
   TABLE DATA           <   COPY public."Student_Group" (id_student, shifr) FROM stdin;
    public               postgres    false    221   4)       �           0    0    Class_id_class_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public."Class_id_class_seq"', 17, true);
          public               postgres    false    223            3           2606    16508    Group Group_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."Group"
    ADD CONSTRAINT "Group_pkey" PRIMARY KEY (shifr);
 >   ALTER TABLE ONLY public."Group" DROP CONSTRAINT "Group_pkey";
       public                 postgres    false    218            9           2606    16510 !   Student_Group Student_ Group_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public."Student_Group"
    ADD CONSTRAINT "Student_ Group_pkey" PRIMARY KEY (id_student, shifr);
 O   ALTER TABLE ONLY public."Student_Group" DROP CONSTRAINT "Student_ Group_pkey";
       public                 postgres    false    221    221            0           2606    16512    Class cls_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public."Class"
    ADD CONSTRAINT cls_pkey PRIMARY KEY (id_class);
 :   ALTER TABLE ONLY public."Class" DROP CONSTRAINT cls_pkey;
       public                 postgres    false    217            ;           2606    16600    Course course_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public."Course"
    ADD CONSTRAINT course_pkey PRIMARY KEY (id_course);
 >   ALTER TABLE ONLY public."Course" DROP CONSTRAINT course_pkey;
       public                 postgres    false    222            5           2606    16573    Professor pro_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."Professor"
    ADD CONSTRAINT pro_pkey PRIMARY KEY (id_professor);
 >   ALTER TABLE ONLY public."Professor" DROP CONSTRAINT pro_pkey;
       public                 postgres    false    219            7           2606    16520    Student stud_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public."Student"
    ADD CONSTRAINT stud_pkey PRIMARY KEY (id_student);
 =   ALTER TABLE ONLY public."Student" DROP CONSTRAINT stud_pkey;
       public                 postgres    false    220            1           1259    16583    fki_P    INDEX     C   CREATE INDEX "fki_P" ON public."Class" USING btree (id_professor);
    DROP INDEX public."fki_P";
       public                 postgres    false    217            <           2606    16578    Class Class_id_professor_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Class"
    ADD CONSTRAINT "Class_id_professor_fkey" FOREIGN KEY (id_professor) REFERENCES public."Professor"(id_professor) NOT VALID;
 K   ALTER TABLE ONLY public."Class" DROP CONSTRAINT "Class_id_professor_fkey";
       public               postgres    false    4661    217    219            =           2606    16531    Class Class_shifr_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Class"
    ADD CONSTRAINT "Class_shifr_fkey" FOREIGN KEY (shifr) REFERENCES public."Group"(shifr) NOT VALID;
 D   ALTER TABLE ONLY public."Class" DROP CONSTRAINT "Class_shifr_fkey";
       public               postgres    false    217    218    4659            >           2606    16620    Group Group_id_course_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Group"
    ADD CONSTRAINT "Group_id_course_fkey" FOREIGN KEY (id_course) REFERENCES public."Course"(id_course) NOT VALID;
 H   ALTER TABLE ONLY public."Group" DROP CONSTRAINT "Group_id_course_fkey";
       public               postgres    false    222    218    4667            ?           2606    16541 ,   Student_Group Student_ Group_id_student_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Student_Group"
    ADD CONSTRAINT "Student_ Group_id_student_fkey" FOREIGN KEY (id_student) REFERENCES public."Student"(id_student);
 Z   ALTER TABLE ONLY public."Student_Group" DROP CONSTRAINT "Student_ Group_id_student_fkey";
       public               postgres    false    220    4663    221            @           2606    16546 '   Student_Group Student_ Group_shifr_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Student_Group"
    ADD CONSTRAINT "Student_ Group_shifr_fkey" FOREIGN KEY (shifr) REFERENCES public."Group"(shifr);
 U   ALTER TABLE ONLY public."Student_Group" DROP CONSTRAINT "Student_ Group_shifr_fkey";
       public               postgres    false    4659    218    221            �   �   x�m��	�@���N602o�zH-#"�x�x�A���t�BDD�9��~ ��J-kcx�Xk�8��1:�'^x�\]m�)�q�Iмe=|�glY��q���рH,U��Fϣ �����W�<�1�Kt�Y�� KJ�      �   �   x����
�PE��+�K_�����Ipu֢���[���?�/�j����?2U�v�8dǅ�:��ˑo�ﲗDR����6>��$)W�ڌ��x��k�N�v8���h)t���%�$�^tf�P��;׫��+�b"B�����H�l/�u:h�[�U�e*�&M����ە�      �   X   x�u���@C�apx�.Nv1�#i.���~4ym�򓴀����F��X�sM
��U%�oU@��U��KT����F&������7��*�      �   �   x�32�503�0�¦.콰��&GY�����F�&�f朙e�y�e���9zE�\F ���� dl��pa녝�3��7��P���v_�t��b��nNC�L+ίJIC�����|Ӆ=�F��	W���� �i      �   �  x�ERMKA=W�O-�_3ݷ��\��]�`�ū�A{PrJ$x1H Y� *�_��G����c`�ޛ�HI'FJ`�u�u���6_��_@�$U��X��b���p��hv�i��
N�իU�j���6�Y ��	_p�G�$)ȗ�7,������B/��֔łA)�n����Qbd�R�@����;�����Q
8��qS��j���K���C���u܊3�O�v"8)`��w]-p�����y.bf��:-�:��X�|��:)�{(������!;�4주��5�gg<�-��o�����襦��Y�R�V���*���C?���	�
AB�����NM���"�i7to��p�0�Psf3���*c���r[n _ѵ�rF[��b�W4�_y򱑂i�|g>Ķ�?�q��t`�}��}��?��      �      x���Ե!KK��/��52����� R�L     