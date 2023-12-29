create table courses
(
    short_name text primary key,
    name       text,
    block      int,
    credits    int
);

insert into courses
values ('ML1', 'Machine Learning 1', 1, 6),
       ('CV1', 'Computer Vision 1', 1, 6),
       ('DL1', 'Deep Learning 1', 2, 6),
       ('NLP1', 'Natural Language Processing 1', 2, 6),
       ('FACT', 'Fairness Accountability Confidentiality and Transparency in AI', 3, 6),
       ('IR1', 'Information Retrieval 1', 4, 6),
       ('KRR', 'Knowledge Representation and Reasoning', 2, 6),

       ('AIM', 'AI for Medical Imaging', 1, 6),
       ('DL4NLP', 'Deep Learning for Natural Language Processing', 1, 6),
       ('ML2', 'Machine Learning 2', 1, 6),
       ('RL', 'Reinforcement Learning', 1, 6),

       ('C', 'Causality', 2, 6),
       ('CLTLKR', 'Computational Learning Theory, Logic and Knowledge Representation', 2, 6),
       ('CSC', 'Computational Social Choice', 2, 6),
       ('HitLML', 'Human-in-the-Loop Machine Learning', 2, 6),
       ('IR2', 'Information Retrieval 2', 2, 6),
       ('IT', 'Information Theory', 2, 6),

       ('ATCS', 'Advanced Topics in Computational Semantics', 5, 6),
       ('AP', 'Automated Planning', 5, 6),
       ('CV2', 'Computer Vision 2', 5, 6),
       ('DL2', 'Deep Learning 2', 5, 6),
       ('GT', 'Game Theory', 5, 6),
       ('NLP2', 'Natural Language Processing 2', 5, 6),

       ('IE', 'Interpretability & Explainability in AI', 6, 6),
       ('MA', 'Multimedia Analytics', 6, 6),
       ('RS', 'Recommender Systems', 6, 6),

       ('AGT', 'Algorithmic Game Theory', 1, 6),
       ('EC', 'Evolutionary Computing', 1, 6),
       ('NDDL', 'Neural Dynamics and Deep Learning', 2, 6),
       ('DDBIE', 'Data-Driven Business Innovation and Entrepreneurship', 4, 6),
       ('MLT', 'Machine Learning Theory', 4, 8),
       ('DMT', 'Data Mining Techniques', 5, 6);

create table reviews
(
    uuid              text primary key,
    email             text,
    nickname          text,
    course_short_name text,
    date              datetime,
    year              text,
    rating            int,
    difficulty        int,
    workload          int,
    review            text,
    is_verified       bool,

    foreign key (course_short_name) references courses (short_name)
);
