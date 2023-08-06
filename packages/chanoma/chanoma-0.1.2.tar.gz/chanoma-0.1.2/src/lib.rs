use pyo3::exceptions::PyOSError;
use pyo3::prelude::*;
use pyo3::wrap_pymodule;

mod characters_set;
use characters_set::*;

#[pyclass]
struct Chanoma {
    c: chanoma::Chanoma,
}

#[pymethods]
impl Chanoma {
    #[new]
    #[args(
        table = "None",
        neologdn = "false",
        preset = "false",
        rc = "false",
        configfile = "None"
    )]
    fn new(
        table: Option<&Table>,
        neologdn: bool,
        preset: bool,
        rc: bool,
        configfile: Option<&str>,
    ) -> PyResult<Self> {
        let mut c = if let Some(file) = configfile {
            chanoma::Chanoma::from_config_file(file)
                .map_err(|e| PyOSError::new_err(e.to_string()))?
        } else if rc {
            chanoma::Chanoma::load_rc().map_err(|e| PyOSError::new_err(e.to_string()))?
        } else {
            chanoma::Chanoma::new()
        };
        if let Some(table) = table {
            c.add_table(table.t.clone());
        }
        if preset {
            c.use_preset();
        }
        if neologdn {
            c.use_neologdn();
        }
        Ok(Self { c })
    }

    fn normalize(&self, text: &str) -> String {
        self.c.normalize(text)
    }
}

#[pyclass]
#[derive(Clone)]
struct Item {
    from: String,
    to: String,
}

#[pymethods]
impl Item {
    #[new]
    fn new(from: String, to: String) -> Self {
        Self { from, to }
    }
}

impl From<&chanoma::Item> for Item {
    fn from(f: &chanoma::Item) -> Self {
        Self {
            from: f.from.clone(),
            to: f.to.clone(),
        }
    }
}

impl From<&Item> for chanoma::Item {
    fn from(f: &Item) -> Self {
        Self {
            from: f.from.clone(),
            to: f.to.clone(),
        }
    }
}

#[pyclass]
struct Correspondence {
    #[pyo3(get)]
    items: Vec<Item>,
}

#[pymethods]
impl Correspondence {
    #[new]
    pub fn new(items: Vec<Item>) -> Self {
        Self { items }
    }
}

#[derive(FromPyObject)]
struct CorrespondenceExtraction {
    items: Vec<Item>,
}

impl CorrespondenceExtraction {
    pub fn items(&self) -> Vec<Item> {
        self.items.clone()
    }
}

impl From<&CorrespondenceExtraction> for chanoma::Correspondence<chanoma::Synthesized> {
    fn from(f: &CorrespondenceExtraction) -> Self {
        Self::new(chanoma::Synthesized::new(
            f.items()
                .iter()
                .map(chanoma::Item::from)
                .collect::<Vec<chanoma::Item>>(),
        ))
    }
}

#[pyclass]
struct Table {
    pub t: chanoma::Table,
}

#[pymethods]
impl Table {
    #[new]
    #[args(preset = "false", csv = "None", yaml = "None")]
    fn new(preset: bool, csv: Option<&str>, yaml: Option<&str>) -> PyResult<Self> {
        let mut t = chanoma::TableBuilder::new();
        if preset {
            t.preset();
        }
        if let Some(csv_path) = csv {
            t.add_from_csv(csv_path)
                .map_err(|e| PyOSError::new_err(e.to_string()))?;
        }
        if let Some(yaml_path) = yaml {
            t.add_from_yaml(yaml_path)
                .map_err(|e| PyOSError::new_err(e.to_string()))?;
        }
        Ok(Self {
            t: t.build().clone(),
        })
    }

    fn add(&mut self, corr: &PyAny) -> PyResult<()> {
        let corr: CorrespondenceExtraction = corr.extract()?;
        self.t.add(&chanoma::Correspondence::from(&corr));
        Ok(())
    }
}

#[pymodule]
fn chanoma(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Chanoma>()?;
    m.add_class::<Table>()?;
    m.add_class::<Item>()?;
    m.add_class::<Correspondence>()?;
    m.add_wrapped(wrap_pymodule!(characters_set))?;

    Ok(())
}
